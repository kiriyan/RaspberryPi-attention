from multiprocessing import Process, Queue
import utils.AudioPlayer as ap
from utils.Screen import *

class ProcessPool:
    AudioTasks = Queue()  # 音频任务表，传入歌曲名str
    ScreenTasks = Queue()  # 屏幕任务表
    procMain = None  # Process(target=Mainloop, args=(AudioTasks,))
    procAudio = None
    procScreen = None

    def __init__(self, mainloop=None):
        """
        把主函数传入，作为主进程;把屏幕刷新函数传入（可选）
        :param mainloop: 必须包含两个传入参数AudioTasks, ScreenTasks
        :param ScreenFunc: 必须包含一个传入参数ScreenTasks
        """
        ProcessPool.procAudio = Process(target=self.AudioProc, args=(ProcessPool.AudioTasks,))
        ProcessPool.procMain = Process(target=mainloop, args=(ProcessPool.AudioTasks, ProcessPool.ScreenTasks,))
        ProcessPool.procScreen = Process(target=self.AudioProc, args=(ProcessPool.ScreenTasks,))
        self.Screen = Screen()
        # if ScreenFunc is not None:
        #     ProcessPool.procScreen = Process(target=ScreenFunc, args=(ProcessPool.ScreenTasks,))
        self.AudioNowTask = None

    def AudioProc(self, tasks=Queue()):
        """
        音乐播放器进程
        :param tasks: AudioTasks()
        :return:
        """
        while True:
            if not tasks.empty():
                file_name = tasks.get()
                print("playing: ", file_name)
                if self.AudioNowTask is not None:
                    try:
                        self.AudioNowTask.terminate()
                    except:
                        print("audioNowPlay close error")
                    else:
                        print("audioNowPlay closed")
                self.AudioNowTask = ap.playMusic(file_name)
                self.AudioNowTask.start()

    def ScreenProc(self, tasks=Queue()):
        while True:
            if not tasks.empty():
                order = tasks.get()
                print("order: ", order)
                if order["name"] == "Jump":
                    self.Screen.drawImg(order["args"]["page"])
                elif order["name"] == "set_attention":
                    self.Screen.set_attention(order["args"]["val"])

    def startMain(self):
        """
        启动主函数进程
        :return:
        """
        print("start main")
        ProcessPool.procMain.start()

    def startAudio(self):
        """
        启动音频播放器进程
        :return:
        """
        ProcessPool.procAudio.start()

    def startAll(self):
        """
        同时启动主函数和音频启动器进程
        :return:
        """
        ProcessPool.procMain.start()
        ProcessPool.procAudio.start()
        ProcessPool.procScreen.start()