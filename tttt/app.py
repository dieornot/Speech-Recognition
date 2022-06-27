import speech_recognition as sr
import win32com.client
import requests
import json
import random
import string
import hashlib
import win32api
import psutil
import pymysql
import datetime
from aip import AipSpeech
import os
from flask import Flask, request,render_template,jsonify, session


# 音频文件转文字：采用百度的语音识别python-SDK 所需参数
APP_ID = '26027667'
API_KEY = 'tKV15wFXZK4nMG8xkmmVdlsa'
SECRET_KEY = 'Sduu8APGOlTA5cGVETUEhlpt4yx1dk6A'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
path = 'recording.wav'

#调用图灵机器人所需参数
turing_api_key = "0e67394f0d3e44ccb54d426928fabf23"
api_url = "http://openapi.tuling123.com/openapi/api/v2"
headers = {'Content-Type':'application/json;charset=UTF-8'}

# 连接数据库
connection = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="aiaudio")
cursor = connection.cursor()

#创建应用对象
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
speaker = win32com.client.Dispatch("SAPI.SpVoice")

#开始页面路由
@app.route('/')
def index():
    return render_template('index.html')

# 注册功能路由
@app.route('/register', methods=["POST"])
def register():
    # 获取前端发送的注册用户的用户名
    username = request.form.get("username")
    # print(username)
    sql5 = "SELECT * FROM login WHERE username = '%s' " % username
    if (cursor.execute(sql5) == 1):
        # print(0)
        return "0"
    #验证密码和确认密码是否一致
    password = request.form.get("password")
    passwordok = request.form.get("passwordok")
    if password != passwordok:
        # print(-1)
        return "-1"
    # 获取前端发送的注册用户的密码
    else:
        password = request.form.get("password")

        if bool(username) & bool(password):

            # 生成哈希盐值
            salt = "".join(random.sample(string.ascii_letters + string.digits, 16))
            # md5加密
            hashPassword = hashlib.sha256((password + salt).encode("utf8")).hexdigest()
            # 将用户信息保存到数据库
            sql = "insert into login value (null, '" + username + "', '" + str(
                hashPassword) + "', '" + salt + "')"
            cursor.execute(sql)
        else:
            # print(2)
            return "2"
        # 提交数据库事务
        connection.commit()
        if (cursor.execute(sql5) == 1):
            # print(1)
            return "1"
        else:
            # print(3)
            return "3"


# 密码登录功能路由
@app.route('/passwordLogin', methods=["POST"])
def passwordLogin():
    # print("seccess")
    # 获取前端表单输入的用户名
    username = request.form.get("username")
    # print(username)
    # 获取前端表单输入的密码
    password = request.form.get("password")
    # yzm1 = request.form.get("yzm")
    # yzm2 = request.form.get("YZM")
    # print(yzm1,yzm2)
    # if yzm1 != yzm2:
    #     return "<script>alert('验证码错误！！');" \
    #            "window.location.href='./static/passwordLogin.html'</script>"
    # 根据用户名查询数据库内的数据
    sql = "select * from login where username = %s "
    # 执行sql语句
    count = cursor.execute(sql, [username])
    # print(count)
    # 如果没有对应的用户名，返回界面重新登录
    if count == 0:
        return "-1"
    # 移动游标到下一行数据
    login = cursor.fetchone()
    # 获得到的用户密码和盐值
    selectedPassword = login[2]
    selectedSalt = login[3]
    selectuser_id = login[0]
    selectuser_name = login[1]
    # print(selectuser_id)
    if not hashlib.sha256((password + selectedSalt).encode("utf8")).hexdigest() == selectedPassword:
        return "0"
    else:
        # 登录日志记录
        selectlogin_time = datetime.datetime.now()
        type2 = 'passwordlogin'
        # print(selectuser_id, selectuser_name, selectlogin_time)
        sql1 = "insert into loginmessage values (null, %d, '%s', '%s', '%s') " % (
            selectuser_id, selectuser_name, selectlogin_time, type2)
        cursor.execute(sql1)
        connection.commit()
        session['name'] = selectuser_name
        return "1"


#语音日志记录
def msgsave(result):
    username = session['name']
    usersay = list(result.values())[0]
    aisay = list(result.values())[1]
    time = datetime.datetime.now()
    #写入数据库
    sql = "insert into speakmsg values (null, '%s', '%s', '%s', '%s') " \
          % (username, usersay, aisay, time)
    cursor.execute(sql)
    connection.commit()
    # print(username, aisay, usersay, time)


#语音日志查询路由
@app.route("/speakmsg",methods=["GET"])
def speakmsg():
    username = session['name']
    # print(username)
    sql = "select * from speakmsg where username = %s "
    cursor.execute(sql,[username])
    speakmsg = cursor.fetchall()
    return jsonify(speakmsg)




#开始说话
@app.route('/aiaudio',methods=["GET"])
def aiaudio():
    my_record()
    result = totext()
    # speaker.Speak(list(result.values())[1])
    return result

# 语音播报
@app.route('/aispeaker',methods=["POST"])
def aispeaker():
    data = request.form.get("aiWords")
    speaker.Speak(data)
    return 'succese'

#启动程序
def start(exe):
        if "音乐" in exe:
            # 打开音乐
            win32api.ShellExecute(0, 'open', 'cloudmusic.exe', '', '', 1)
            result = "已为您启动音乐"
            # speaker.Speak("以为您启动音乐")
            return result
        if "浏览器" in exe:
            win32api.ShellExecute(0, 'open', 'msedge.exe', '', '', 1)
            # speaker.Speak("以为您启动浏览器")
            result = "已为您启动浏览器"
            return result
        if "计算器" in exe:
            win32api.ShellExecute(0, "open", "calc.exe", '', '', 1);
            result = "以为您启动计算器"
            return result
        if "记事本" in exe:
            win32api.ShellExecute(0, "open", "notepad.exe", '', '', 1);
            result = "以为您启动记事本"
            return result
        else:
            result = "没有找到预设的程序"
            return result
#关闭程序
def shutdown(exe):
        if "音乐" in exe:
            TARGET = "cloudmusic.exe"
            [process.kill() for process in psutil.process_iter() if process.name() == TARGET]
            # speaker.Speak("以为您关闭音乐")
            result = "已为您关闭音乐"
            return result
        if "浏览器" in exe:
            TARGET = "msedge.exe"
            [process.kill() for process in psutil.process_iter() if process.name() == TARGET]
            # speaker.Speak("以为您关闭浏览器")
            result = "已为您关闭浏览器"
            return result
        if "计算器" in exe:
            TARGET = "calc.exe"
            [process.kill() for process in psutil.process_iter() if process.name() == TARGET]
            result = "以为您关闭计算器"
            return result
        if "记事本" in exe:
            TARGET = "notepad.exe"
            [process.kill() for process in psutil.process_iter() if process.name() == TARGET]
            result = "以为您关闭记事本"
            return result
        else:
            result = "没有找到预设的程序"
            return result
# 使用语音识别包录制音频
def my_record(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("请说点什么。")
        speaker.Speak("请说点什么。")
        audio = r.listen(source)
    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())
    print("录音完成")
    speaker.Speak("录音完成。")

#读取语音转文字
def totext():
    # 读取录音文件
    with open(path, 'rb') as fp:
        voices = fp.read()
    try:
        # time.sleep(5)
        result = client.asr(voices, 'wav', 16000)
        print(result)
        result_text = result["result"][0]
        print("you said:" + result_text)
        if "打开" in result_text:
            
            # 启动程序
            aiResult =  start(result_text)
            print("AI Robot said: " + aiResult)
        elif "关闭" in result_text:
            # 关闭程序
            aiResult = shutdown(result_text)
            print("AI Robot said: " + aiResult)
        elif "什么是" in result_text:
            aiResult = keywordsearch(result_text)
        else:
            #图灵机器人回复
            # print("turing")
            aiResult = Turing(result_text)
            # print("AI Robot said: " + aiResult)
            # speaker.Speak(aiResult)
        list = {'words': result_text, 'aiWords': aiResult}
        #记录对话日志，写入数据库
        msgsave(list)
        return list

    except KeyError:
        print("KeyError")
        list = {'words': ' ', 'aiWords': "我没有听清楚，请再说一遍..."}
        # speaker.Speak("我没有听清楚，请再说一遍...")
        return list

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
     # print(response_dict)
     result = response_dict["results"][0]["values"]["text"]
     print("AI Robot said: " + result)
     return result

# 关键词百科查询功能
def keywordsearch(result2):
    import requests
    from bs4 import BeautifulSoup
    j = result2.find("什么是")
    k = result2.find('?')
    keywrd = result2[j+3:k]
    URL = f'https://baike.baidu.com/item/{keywrd}'
    headers = \
        {'User-Agent':
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/94.0.4606.81 Safari/537.36'}
    resp = requests.get(url=URL, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'UTF-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        if soup.select_one(
            'body > div.body-wrapper > div.content-wrapper > div'
            ' > div.main-content.J-content > div.lemma-summary > div:nth-child(1)')!= None:
            result = soup.select_one(
                'body > div.body-wrapper > div.content-wrapper > div'
                ' > div.main-content.J-content > div.lemma-summary > div:nth-child(1)').text
            result1 = ''
            for i in result:
                result1 += i
                if i == '。':
                    break
            print("AI Robot said: " + result1)
            return result1
        else:
            print("未查到相关内容，由图灵机器人回答")
            # 图灵机器人回复
            # print("turing")
            aiResult = Turing(result2)
            return aiResult


if __name__ == "__main__":
    app.run()

