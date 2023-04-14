# import utils.Bluetooth as BT
from multiprocessing import Process, Queue
from utils.WebRequest import *
from ProcessPool import *
import random
import os
import time
import serial
import wiringpi
# from bluezero import adapter

OUTPUT = 1  # 定义OUTPUT为1即输出
INPUT = 0  # 定义INPUT为0即输入
HIGH = 1  # 定义HIGH为1即高点平
LOW = 0  # 定义HIGH为1即高点平

wiringpi.wiringPiSetup()  # 设置GPIO编号为wPi方式
# ser_HC05 = serial.Serial('/dev/ttyUSB0',9600,timeout = 0.5)   #使用USB连接串行口

global PinsInput
global saveIndex, uploadIndex, level, wifiName, wifiPass, userID
global Car_State, BlueToothConnected
Car_State = 0
BlueToothConnected = False
PinsInput = [0]
PinsOutput = [2]
userID = "o1JHJ4mbPNY_gv0RvAWw-_zm_WqM"

def ReadOneLine(file_name=""):
    file = open(file=os.getcwd() + "/user/" + file_name)
    val = file.readline()
    file.close()
    return val

def upload():
    # 通过wifi积压上传，未判断状态
    global Car_State, BlueToothConnected, uploadIndex, saveIndex
    if Car_State == 0 and uploadIndex < saveIndex:
        for i in range(uploadIndex+1, saveIndex+1):
            # 从uploadIndex+1到saveIndex
            data = {"id": "", "graph": "", "mark": 0, "gold": "0", "time": 0}
            uploading_path = os.getcwd() + "/user/" + str(i) + ".txt"
            uploading_money_name_str = str(i) + "_money.txt"
            uploading_time_name_str = str(i) + "_time.txt"
            data["mark"] = i
            data["id"] = "o1JHJ4mbPNY_gv0RvAWw-_zm_WqM"
            data["gold"] = int(ReadOneLine(uploading_money_name_str))
            data["time"] = int(ReadOneLine(uploading_time_name_str))
            count_line = 0
            for line in open(uploading_path):
                if count_line != 0:
                    data["graph"] += ","
                data["graph"] += line[0:-1]
                count_line += 1
            res = post(data=data, url="/api/cart/upload")
            if res.__contains__('error'):
                print(res["error"])
                time.sleep(1)
            elif res["success"]:
                uploadIndex = i
                file = open(file=os.getcwd() + "/user/UploadIndex.txt", mode="w")
                print(uploadIndex, end="", file=file)
            else:
                time.sleep(1)
            print(res)
            # time.sleep(3)
            # print(data["graph"])

def connectedTest(self):
    global BlueToothConnected
    print("testConnected")
    BlueToothConnected = True


def disconnectedTest(self):
    global BlueToothConnected
    print("testDisconnected")
    BlueToothConnected = False


def receiveTest(self, value):
    print(value)

def setup():
    # adapter_address = list(adapter.Adapter.available())[0].address
    # bluetooth = BT.BlueService(adapter_address)
    # bluetooth.publish()
    global saveIndex, uploadIndex, PinsInput
    for pin in PinsInput:
        wiringpi.pinMode(pin, INPUT)  # 设置GPIO_Intput_Pin为INPUT输入模式
    for pin in PinsOutput:
        wiringpi.pinMode(pin, OUTPUT)  # 设置GPIO_Intput_Pin为INPUT输入模式
    wiringpi.digitalWrite(PinsOutput[0], LOW)
    saveIndex = int(ReadOneLine("SaveIndex.txt"))
    uploadIndex = int(ReadOneLine("UploadIndex.txt"))
    level = int(ReadOneLine("level.txt"))
    wifiName = ReadOneLine("WifiName.txt")
    wifiPass = ReadOneLine("WifiPass.txt")
    print("save =", saveIndex)
    print("upload =", uploadIndex)
    print("level =", level)
    print("wifiname =", wifiName)


def pd_WakeUp():
    if wiringpi.digitalRead(PinsInput[0]) == HIGH:
        wake_up_time = time.time()
        while time.time() - wake_up_time <= 2:
            if wiringpi.digitalRead(PinsInput[0]) == LOW:
                return False
        return True
    return False

def pid(attention=50):
    """
    【期望】读取模拟引脚返回灰度值，pid算法输出pwm波循迹
    【实际】串口输出attention
    :param attention:
    :return:
    """
    pass

def Mainloop(AudioTasks=Queue(), ScreenTasks=Queue()):
    global Car_State
    attentions = []
    setup()
    last_state = 0
    threshold = 45
    now_wifi_time = time.time()
    now_update_time = time.time()
    attention_index = 0
    while True:
        # print("3(左).mp3")
        # AudioTasks.put("3(左).mp3")
        # time.sleep(10)
        # print("4(右).mp3")
        # AudioTasks.put("4(右).mp3")
        # time.sleep(10)
        if Car_State == 0:
            # 休眠模式
            wiringpi.digitalWrite(PinsOutput[0], LOW)
            upload()
            if time.time() - now_wifi_time >= 2:
                data = {"id": userID, "dot": -1}
                res = post(data=data, url="/api/cart/updateDot")
                print(res)
                now_wifi_time = time.time()
            pd = pd_WakeUp()
            if pd:
                Car_State = 1
                time.sleep(1)

        elif Car_State == 1:
            # 训练准备模式
            wiringpi.digitalWrite(PinsOutput[0], LOW)
            file_path = os.getcwd() + "/static/graph/points.txt"
            attention_file = open(file_path)
            attention_strs = attention_file.readline().split(',')
            for str in attention_strs:
                attentions.append(int(str))

        elif Car_State == 2:
            wiringpi.digitalWrite(PinsOutput[0], HIGH)
            if time.time() - now_update_time > 1.:
                now_attention = attentions[attention_index]
                attention_index += 1
                pid(now_attention)
                scnOrder = {"name": "Jump", "args": {"page": "Page_state1.jpg"}}
                ScreenTasks.put(scnOrder)
                scnOrder = {"name": "set_attention", "args": {"val": now_attention}}
                ScreenTasks.put(scnOrder)
                if last_state == -1 and now_attention >= threshold:
                    AudioTasks.put("frog_up.mp3")
                    scnOrder = {"name": "Jump", "args": {"page": "level_up.jpg"}}
                    ScreenTasks.put(scnOrder)
                data = {"id": userID, "dot": now_attention}
                res = post(data=data, url="/api/cart/updateDot")
                if not res.__contains__('error'):
                    threshold = res["content"]["threshold"]
                if now_attention < threshold:
                    last_state = -1
                else:
                    last_state = 1
                now_update_time = time.time()
            if pd_WakeUp():
                Car_State = 1

if __name__ == "__main__":
    PP = ProcessPool(mainloop=Mainloop)
    PP.startAll()
    # setup()


