import wiringpi


GPIO_Intput_Pin = 0  # 定义GPIO_Intput_Pin为1脚
OUTPUT = 1  # 定义OUTPUT为1即输出
INPUT = 0  # 定义INPUT为0即输入
HIGH = 1  # 定义HIGH为1即高点平
LOW = 0  # 定义HIGH为1即高点平

wiringpi.wiringPiSetup()  # 设置GPIO编号为wPi方式
wiringpi.pinMode(GPIO_Intput_Pin, INPUT)  # 设置GPIO_Intput_Pin为INPUT输入模式

while 1:
    print('GPIO_Intput_Pin INPUT <=', wiringpi.digitalRead(GPIO_Intput_Pin))  # 打印从GPIO_Intput_Pin读到的数据
    wiringpi.delay(1000)  # 延时1000ms
    print()  # 为了输出美观 打印换行
