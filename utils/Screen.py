# coding : UTF-8
"""
屏幕组件
"""
import time  # 用于计算spi刷新整个屏幕所用时长
import RPi.GPIO as GPIO  # 用于操作引脚
import spidev  # 树莓派与屏幕的交互协议为SPI，说明见：https://github.com/doceme/py-spidev
from PIL import Image, ImageFont, ImageDraw  # 用于创建画布，或者读取具体路径下的图片。给图片添加文字。
import os

class Screen:
    
    screenWidth = 320  # 屏幕长度
    screenHeight = 240  # 屏幕宽度
    PinDC = 18  # GPIO.BOARD引脚模式，第18号引脚
    PinReset = 22  # GPIO.BOARD引脚模式，第22号引脚
    PinLED = 12  # GPIO.BOARD引脚模式，第12号引脚
    spi = None

    def LCDReset(self):  # 重置电平时序
        GPIO.output(Screen.PinReset, 1)
        time.sleep(.2)
        GPIO.output(Screen.PinReset, 0)
        time.sleep(.2)
        GPIO.output(Screen.PinReset, 1)
        time.sleep(.2)

    def sendCommand(self, command, *bytes):  # 发送指令（DC为低电平）和数据（DC为高电平）
        GPIO.output(Screen.PinDC, 0)
        Screen.spi.writebytes([command])
        if len(bytes) > 0:
            GPIO.output(Screen.PinDC, 1)
            Screen.spi.writebytes(list(bytes))

    def sendManyBytes(self, bytes):  # 发送屏幕数据
        GPIO.output(Screen.PinDC, 1)
        Screen.spi.writebytes(bytes)

    def init(self):  # 屏幕初始化
        GPIO.output(Screen.PinLED, 1)  # LED.high();
        self.LCDReset()
        self.sendCommand(0xEF, 0x03, 0x80, 0x02)
        self.sendCommand(0xCF, 0x00, 0XC1, 0X30)
        self.sendCommand(0xED, 0x64, 0x03, 0X12, 0X81)
        self.sendCommand(0xE8, 0x85, 0x00, 0x78)
        self.sendCommand(0xCB, 0x39, 0x2C, 0x00, 0x34, 0x02)
        self.sendCommand(0xF7, 0x20)
        self.sendCommand(0xEA, 0x00, 0x00)
        self.sendCommand(0xC0, 0x23)  # Power control --VRH[5:0]
        self.sendCommand(0xC1, 0x10)  # Power control # SAP[2:0];BT[3:0]
        self.sendCommand(0xC5, 0x3e, 0x28)  # VCM control
        self.sendCommand(0xC7, 0x86)  # VCM control2
        self.sendCommand(0x36, 0x48)  # Memory Access Control
        self.sendCommand(0x3A, 0x55)
        self.sendCommand(0xB1, 0x00, 0x18)
        self.sendCommand(0xB6, 0x08, 0x82, 0x27)  # Display Function Control
        self.sendCommand(0xF2, 0x00)  # 3Gamma Function Disable
        self.sendCommand(0x26, 0x01)  # Gamma curve selected
        self.sendCommand(0xE0, 0x0F, 0x31, 0x2B, 0x0C, 0x0E, 0x08, 0x4E, 0xF1, 0x37, 0x07, 0x10, 0x03, 0x0E, 0x09,
                    0x00)  # Set Gamma
        self.sendCommand(0xE1, 0x00, 0x0E, 0x14, 0x03, 0x11, 0x07, 0x31, 0xC1, 0x48, 0x08, 0x0F, 0x0C, 0x31, 0x36,
                    0x0F)  # Set Gamma
        self.sendCommand(0x11)  # Exit Sleep
        self.sendCommand(0x29)  # Display on

    def setWindow(self):
        self.sendCommand(0x2A)  # Column addr set
        x0 = 0
        bytes = []
        bytes.append(x0 >> 8)
        bytes.append(x0)
        self.sendManyBytes(bytes)  # XSTART
        x1 = Screen.screenHeight - 1
        bytes = []
        bytes.append(x1 >> 8)
        bytes.append(x1)
        self.sendManyBytes(bytes)  # XEND
        self.sendCommand(0x2B)  # Row addr set
        bytes = []
        bytes.append(0 >> 8)
        bytes.append(0)
        self.sendManyBytes(bytes)  # YSTART
        y1 = Screen.screenWidth - 1
        bytes = []
        bytes.append(y1 >> 8)
        bytes.append(y1)
        self.sendManyBytes(bytes)  # YEND
        self.sendCommand(0x2C)
        print('setWindow donw')

    def drawImg16BitColor(self, img320x240):  # 入参为320x240像素的image对象
        self.init()
        self.setWindow()
        bytes = []
        i = 0
        GPIO.output(Screen.PinDC, 1)
        picReadStartTime = time.time()
        for x in range(0, Screen.screenWidth):
            for y in range(Screen.screenHeight - 1, -1, -1):
                colorValue = img320x240.getpixel((x, y))
                red = colorValue[0]
                green = colorValue[1]
                blue = colorValue[2]
                red = red >> 3  # st7735s的红色占5位
                green = green >> 2  # st7735s的绿色占6位
                blue = blue >> 3  # st7735s的蓝色占5位
                highBit = 0 | (red << 3) | (green >> 3)  # 每个像素写入个字节，highBit高字节，lowBit低字节
                lowBit = 0 | (green << 5) | blue
                bytes.append(highBit)
                bytes.append(lowBit)
        picReadTimeConsuming = time.time() - picReadStartTime  # 解析图像像素时长
        try:
            startTime = time.time()
            # Screen.screenWidth*Screen.screenHeight*2 每个像素写入2个字节。
            # 以下for循环是为了控制每次传入的数组长度，防止这个报错,：OverflowError: Argument list size exceeds 4096 bytes.
            for j in range(2000, Screen.screenWidth * Screen.screenHeight * 2, 2000):
                self.sendManyBytes(bytes[i:j])
                i = i + 2000
            self.sendManyBytes(bytes[i:Screen.screenWidth * Screen.screenHeight * 2])
        except:
            return False
        else:
            SpiTimeConsuming = time.time() - startTime  # Spi写入像素数据时长
            print("picReadTimeConsuming = %.3fs , SpiTimeConsuming = %.3fs" % (picReadTimeConsuming, SpiTimeConsuming))
            return True

    def newPage(self):
        self.image = Image.new('RGB', (Screen.screenWidth, Screen.screenHeight))  # 可以使用代码新建画布
        self.draw = ImageDraw.Draw(self.image)

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)  # 设置GPIO.BOARD引脚模式
        GPIO.setwarnings(False)
        GPIO.setup(Screen.PinDC, GPIO.OUT)
        GPIO.setup(Screen.PinReset, GPIO.OUT)
        GPIO.setup(Screen.PinLED, GPIO.OUT)
        Screen.spi = spidev.SpiDev()  # https://github.com/doceme/py-Screen.spidev
        Screen.spi.open(0, 0)
        Screen.spi.max_speed_hz = 24000000  # 通信时钟最大频率
        Screen.spi.mode = 0x00  # SPI的模式，9341为模式Screen.spi0
        # 显示内容相关
        self.PageIndex = 0  # 显示页面号
        self.draw = None  # 绘制对象
        self.image = None
        self.newPage()

    def drawImg(self, path=''):
        """
        在屏幕上全屏显示特定路径的图片
        :param path : str, 图片的绝对路径
        :return isShowed: bool, 显示成功与否
        """
        # 也可以从地址读取图片文件，并缩放为320x240
        self.image = Image.open(path)
        self.image = self.image.convert('RGBA')
        self.image = self.image.resize((Screen.screenWidth, Screen.screenHeight))  # 也可以从地址读取图片文件，并缩放为160x128
        isShowed = self.drawImg16BitColor(self.image)
        return isShowed

    def drawText(self, text="", font_size=15, position=(0, 0), fill="#000000", direction=None):
        """
        在屏幕特定位置写入文字
        :param text: str，显示的文字
        :param font_size: int，字号
        :param position: tuple，位置
        :param fill: str，16进制颜色码
        :param direction: 文字方向
        :return: isShowed
        """
        self.draw = ImageDraw.Draw(self.image)
        setFont = ImageFont.truetype("/usr/share/fonts/myfont/MSYHBD.TTF", font_size)
        self.draw.text(position, text, font=setFont, fill=fill, direction=direction)
        isShowed = self.drawImg16BitColor(self.image)
        return isShowed

screen = Screen()
screen.drawImg(os.getcwd() + "/static/images/" + "3.jpg")
screen.drawText("hello")