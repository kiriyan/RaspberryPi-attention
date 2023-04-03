#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频播放器组件
"""


from pydub import AudioSegment
from pydub.playback import play
from multiprocessing import Process


def terminate():
    """
    终止播放函数
    :return: 终止是否成功
    """
    try:
        AudioPlayer.audio_process.terminate()
    except Exception as e:
        return False
    return True


def playAudio(file_name, start_time=0):
    """
    播放函数(仅支持wav格式)
    :param file_name: static/audio中文件名
    :param start_time: 播放开始时间(毫秒)
    :return:
    """
    full_clip = AudioSegment.from_wav("../static/audio/" + file_name)
    AudioPlayer.audio_process = Process(play, full_clip[start_time:])
    AudioPlayer.audio_process.start()


class AudioPlayer:

    audio_process = Process()

