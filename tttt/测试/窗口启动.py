import speech_recognition as sr
import win32com.client
from aip import AipSpeech
import requests
import json
import time
import win32api
import psutil
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#启动程序
def start(exe):
    if "打开" in exe:
        if "音乐" in exe:
            # 打开音乐
            win32api.ShellExecute(0, 'open', 'cloudmusic.exe', '', '', 1)
            speaker.Speak("以为您启动音乐")
            return 0
        if "浏览器" in exe:
            win32api.ShellExecute(0, 'open', 'chrome.exe', '', '', 1)
            speaker.Speak("以为您启动浏览器")
            return 0
#关闭程序
def shutdown(exe):
    if "关闭" in exe:
        if "音乐" in exe:
            TARGET = "cloudmusic.exe"
            [process.kill() for process in psutil.process_iter() if process.name() == TARGET]
            speaker.Speak("以为您关闭音乐")
            return 0
        if "浏览器" in exe:
            TARGET = "chrome.exe"
            [process.kill() for process in psutil.process_iter() if process.name() == TARGET]
            speaker.Speak("以为您关闭浏览器")
# 调用计算器
# win32api.ShellExecute(0,"open","calc.exe",'', '', 1);
# 调用记事本
# win32api.ShellExecute(0,"open","notepad.exe",'', '', 1);
speaker.speak("电话[英语：Telephone，出自希腊语τῆλε（tēle，意为“远”）和φωνή（phōnē，意为“声音”），旧译德律风]是一种可以传送与接收声音的远程通信设备。早在18世纪欧洲已有“电话”一词，用来指用线串成的话筒（以线串起杯子）。电话的出现要归功于亚历山大·格拉汉姆·贝尔，早期电话机的原理为：说话声音为空气里的复合振动，可传输到固体上，通过电脉冲于导电金属上传递。")