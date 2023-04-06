#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝牙组件
"""
import time

from bluezero import adapter, peripheral, device

class BlueService:

    connected_method = None

    disconnected_method = None

    receive_method = None

    def __init__(self, adapter_address, receive_method=None, connected_method=None, disconnected_method=None, ):
        """
        构造方法
        构造时传入
        可在下列method中通过self.send()的方式发送数据给手机
        :param adapter_address:
        :param receive_method: 接收到数据时执行 参数有self value; value为接收到的参数
        :param connected_method: 成功连接时执行 参数有self
        :param disconnected_method: 断开连接时执行 参数有self
        """
        UART_SERVICE = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_CHARACTERISTIC = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_CHARACTERISTIC = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        BlueService.receive_method = receive_method
        BlueService.connected_method = connected_method
        BlueService.disconnected_method = disconnected_method

        ble_uart = peripheral.Peripheral(
            adapter_address,
            local_name='Nero_Car_Service'
        )

        ble_uart.add_service(srv_id=1, uuid=UART_SERVICE, primary=True)

        ble_uart.add_characteristic(
            srv_id=1, chr_id=1, uuid=RX_CHARACTERISTIC,
            value=[], notifying=False,
            flags=['write', 'write-without-response'],
            write_callback=self.uart_write,
            read_callback=None,
            notify_callback=None
        )

        ble_uart.add_characteristic(
            srv_id=1, chr_id=2, uuid=TX_CHARACTERISTIC,
            value=[], notifying=False,
            flags=['notify'],
            notify_callback=self.uart_notify,
            read_callback=None,
            write_callback=None
        )

        ble_uart.on_connect = self.on_connect
        ble_uart.on_disconnect = self.on_disconnect

        self.ble_uart = ble_uart
        self.tx_obj = None

    def publish(self):
        self.ble_uart.publish()

    def on_connect(self, ble_device: device.Device):
        print("Connected to " + str(ble_device.address))
        BlueService.connected_method(self)

    def on_disconnect(self, adapter_address, device_address):
        print("Disconnected from " + device_address)
        BlueService.disconnected_method(self)

    def uart_notify(self, notifying, characteristic):
        print("notify_callback")
        if notifying:
            self.tx_obj = characteristic
        else:
            self.tx_obj = None

    def send(self, value):
        """
        蓝牙发送方法
        :param value: str类型的数据
        :return:
        """
        print(self.ble_uart)
        self.ble_uart.characteristics[1].set_value(bytearray(value.encode("UTF-8")))

    def uart_write(self, value, options):
        print('raw bytes:', value)
        BlueService.receive_method(self, value)
        print('With options:', options)
        print('Text value:', bytes(value).decode('utf-8'))


"""
下为使用示例
"""
# def connectedTest(self):
#     print("testConnected")
#     i = 0
#     while True:
#         i += 1
#         time.sleep(1)
#         self.send("ddd" + str(i))
#
#
# def disconnectedTest(self):
#     print("testDisconnected")
#
#
# def receiveTest(self, value):
#     print(value)
#
#
# if __name__ == '__main__':
#     adapter_address = list(adapter.Adapter.available())[0].address
#     ud = BlueService(adapter_address, receiveTest, connectedTest, disconnectedTest)
#     ud.publish()
