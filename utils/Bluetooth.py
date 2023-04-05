#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蓝牙组件
"""
from gi.repository import GLib
from bluezero import adapter, peripheral, device


class UARTDevice:
    def __init__(self, adapter_address):
        UART_SERVICE = 'b0fbf5b2-91eb-4b82-be41-5fb04ddffcb9'
        RX_CHARACTERISTIC = 'b0fbf5b2-91eb-4b82-be41-5fb04ddffcb8'
        TX_CHARACTERISTIC = 'b0fbf5b2-91eb-4b82-be41-5fb04ddffcb7'

        ble_uart = peripheral.Peripheral(
            adapter_address,
            local_name='AttentionGo_RaspberryPi'
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

    def on_disconnect(self, adapter_address, device_address):
        print("Disconnected from " + device_address)

    def uart_notify(self, notifying, characteristic):
        if notifying:
            self.tx_obj = characteristic
        else:
            self.tx_obj = None

    def update_tx(self, value):
        if self.tx_obj:
            print("Sending")
            self.tx_obj.set_value(value)

    def uart_write(self, value, options):
        print('raw bytes:', value)
        print('With options:', options)
        print('Text value:', bytes(value).decode('utf-8'))
        self.update_tx(value)


if __name__ == '__main__':
    adapter_address = list(adapter.Adapter.available())[0].address
    ud = UARTDevice(adapter_address)
    ud.publish()


def getState():
    """
    获取蓝牙状态函数
    :return: 蓝牙是否连接
    """
    return False


def read():
    """
    读取特征值函数
    :return: 当前的特征值
    """
    return ""


def send(str):
    """
    发送字符串函数
    :param str: 待发送字符串
    :return: 发送是否成功
    """
    return True
