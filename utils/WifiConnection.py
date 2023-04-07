# -*-coding:utf-8-*-
import comtypes as comtypes
import pywifi
import time
from pywifi import const
comtypes

# 1、python连接WiFi，需要使用pywifi包，安装pywifi：pip install pywifi
# 注意：如果提示找不到comtypes，则还需要安装pip install comtypes
# 2、判断wifi连接状态：
def wifi_connect_status():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    if iface.status() in [const.IFACE_CONNECTED, const.IFACE_INACTIVE]:
        return True
    else:
        return False


# 3、扫描wifi：
def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()
    time.sleep(1)
    basewifi = iface.scan_results()

    for i in basewifi:
        print("wifi scan result:{}".format(i.ssid))
        print("wifi device MAC address:{}".format(i.bssid))
    return basewifi


# 4、连接指定的wifi：
def connect_wifi(wifiName, wifiPass):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    print(iface.name())  # 输出无线网卡名称
    iface.disconnect()
    time.sleep(3)

    iface.scan()
    currentWifi = iface.scan_results()
    for i in currentWifi:
        if i.ssid == wifiName:
            i.key = wifiPass
            iface.remove_all_network_profiles()  # 删除其它配置文件
            temp = iface.add_network_profile(i)  # 加载配置文件
            iface.connect(temp)
            break

    time.sleep(5)
    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

