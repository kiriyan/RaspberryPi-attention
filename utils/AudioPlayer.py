#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频播放器组件【需要安装pyaudio-- pip install pyaudio】
多进程
"""
import os
from pydub import AudioSegment
from pydub.playback import play
from multiprocessing import Process


def terminatePlaying():
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
    播放函数
    :param file_name: static/audio中文件名
    :param start_time: 播放开始时间(毫秒)
    :return:
    """
    full_clip = AudioSegment.from_file(os.getcwd() + "/static/audio/" + file_name)
    AudioPlayer.audio_process = Process(target=play, args=(full_clip[start_time:],))
    try:
        AudioPlayer.audio_process.start()
    except Exception as e:
        return False
    return True


def playAudioWithoutProcess(file_name, start_time=0):
    """
    不使用多线程的播放函数 无法终止播放
    :param file_name: static/audio中文件名
    :param start_time: 播放开始时间(毫秒)
    :return:
    """
    full_clip = AudioSegment.from_file(os.getcwd() + "/static/audio/" + file_name)
    try:
        play(full_clip[start_time:])
    except Exception as e:
        return False
    return True

def playMusic(file_name):
    """
        播放函数
        :param file_name: static/audio中文件名
        :return: process
        """
    full_clip = AudioSegment.from_file(os.getcwd() + "/static/audio/" + file_name)
    return Process(target=play, args=(full_clip[0:],))

class AudioPlayer:

    audio_process = None

