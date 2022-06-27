# import requests
# import json
# from bs4 import BeautifulSoup
# keywrd = "耳机"
# URL = f'https://baike.baidu.com/item/{keywrd}'
#
# headers = \
#     {'User-Agent':
#          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
# resp = requests.get(url=URL,headers=headers)
# if resp.status_code == 200:
#     resp.encoding = 'UTF-8'
#     soup = BeautifulSoup(resp.text, 'lxml')
#     result =soup.select_one('body > div.body-wrapper > div.content-wrapper > div > div.main-content.J-content > div.lemma-summary > div:nth-child(1)').text
#     result1 = ''
#     for i in result:
#         result1 += i
#         if i == '。':
#             break
#     print(result1)

# 关键词百科查询功能
from flask import session
def keywordsearch(result2):
    from flask import session
    import requests
    from bs4 import BeautifulSoup
    keywrd = result2
    URL = f'https://baike.baidu.com/item/{keywrd}'
    headers = \
        {'User-Agent':
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/94.0.4606.81 Safari/537.36'}
    resp = requests.get(url=URL, headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'UTF-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        result = soup.select_one(
            'body > div.body-wrapper > div.content-wrapper > div > div.main-content.J-content > div.lemma-summary > div:nth-child(1)').text
        result1 = ''
        for i in result:
            result1 += i
            if i == '。':
                break
        return result1

print(keywordsearch("键盘"))
