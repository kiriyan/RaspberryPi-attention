from multiprocessing import Process
import utils.AudioPlayer as ap
import time

time_count = 0
# mp3 = ap.AudioPlayer()
def show(name):
    while True:
        time.sleep(2)
        print("Process name is " + name)

def playMusic(name):
    print("Process name is " + name)
    while True:
        ap.playAudioWithoutProcess("test1.mp3", 0)
        print("hello")
        time.sleep(10)
        ap.playAudioWithoutProcess("test2.mp3", 0)
        time.sleep(10)


if __name__ == "__main__":
    proc1 = Process(target=show, args=('sub1',))
    proc1.start()
    proc2 = Process(target=playMusic, args=('music',))
    proc2.start()
    # result = ap.playAudioWithoutProcess("test1.mp3", 1000)
    # print(result)
    # # ap.playAudio("test1.mp3", 0)
    time.sleep(60)

    # proc.join()