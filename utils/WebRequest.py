import json

import requests

BASE_URL = 'https://chenanbella.cn'
# 测试用URL
# BASE_URL = 'http://localhost:5174'

header = {'Content-Type': 'application/json', 'Content-Length': '<calculated when request is sent>'}
headerFile = {'Content-Type': 'multipart/form-data', 'Content-Length': '<calculated when request is sent>'}


def jsonParse(string):
    return json.loads(string)


def resultHandle(response):
    if response.status_code == 200:
        return jsonParse(response.text)
    else:
        return {'error': response.status_code}


def post(data, url, withFile=False):
    """
    web交互标准post方法
    :param data: 字典对象
    :param url: 后缀url
    :param withFile: 为True代表需要传输文件
    :return: 返回response中的数据字典对象 若出错，会返回{'error': <错误码>}
    """
    if withFile:
        return resultHandle(requests.post(url=BASE_URL + url, json=data, headers=headerFile))
    else:
        return resultHandle(requests.post(url=BASE_URL + url, json=data, headers=header))


