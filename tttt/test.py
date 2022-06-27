# import speech_recognition as sr
# import win32com.client
# from aip import AipSpeech
# import requests
# import json
# import time
# import win32api
# import psutil
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# 使用语音识别包录制音频
def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)
    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())
    print("录音完成")

#音频文件转文字：采用百度的语音识别python-SDK
APP_ID = '26027667'
API_KEY = 'tKV15wFXZK4nMG8xkmmVdlsa'
SECRET_KEY = 'Sduu8APGOlTA5cGVETUEhlpt4yx1dk6A'
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)
path = 'recording.wav'

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
#将语音转文本STT
def listen():
     #读取录音文件
     with open(path,'rb') as fp:
         voices = fp.read()
     try:
         # time.sleep(5)
         result = client.asr(voices,'wav',16000)
         print(result)
         result_text = result["result"][0]
         print("you said:"+result_text)
         #启动程序
         start(result_text)
         #关闭程序
         shutdown(result_text)
         return result_text

     except KeyError:
         print("KeyError")
         speaker.Speak("我没有听清楚，请再说一遍...")

#调用图灵机器人
turing_api_key = "0e67394f0d3e44ccb54d426928fabf23"
api_url = "http://openapi.tuling123.com/openapi/api/v2"
headers = {'Content-Type':'application/json;charset=UTF-8'}

# 图灵机器人回复
def Turing(text_words=""):
     req = {
         "reqType": 0,
         "perception": {
             "inputText": {
                 "text": text_words
             },

             "selfInfo": {
                 "location": {
                     "city": "宜宾",
                     "province": "四川",
                     "street": "石岗路"
                 }
             }
         },
         "userInfo": {
             "apiKey": '0e67394f0d3e44ccb54d426928fabf23',  # 你的图灵机器人apiKey
             "userId": "687948"  # 用户唯一标识(随便填, 非密钥)
         }
     }
     req["perception"]["inputText"]["text"] = text_words
     response = requests.request("post", api_url, json=req, headers=headers)
     response_dict = json.loads(response.text)
     result = response_dict["results"][0]["values"]["text"]
     print("AI Robot said: " + result)
     return result

# 语音合成，输出机器人的回答
my_record()
request = listen()
response = Turing(request)
speaker.Speak(response)


