import os


def getWorkingDir():
    return os.getcwd() + '\\'


def systemOperation(command):
    """
    该方法相当于直接在Terminal执行command
    :param command: 指令str
    :return:
    """
    return os.system(command)


def openPy(pyDir):
    return systemOperation('python3 ' + getWorkingDir() + pyDir)
