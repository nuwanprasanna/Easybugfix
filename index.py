import requests
import json
import base64

def index(urls):
    header = {'Content-Type': 'application/json; charset=utf-8 ', 'Host': 'bing.com'}
    post = {
              "host": "bugsfixing.com",
              "key": "13992d1d1fd54acdb39a75af9a3803a7",
              "keyLocation": "https://www.bugsfixing.com/13992d1d1fd54acdb39a75af9a3803a7.txt",
              "urlList": urls
            }

    responce = requests.post('https://www.bing.com/indexnow', headers = header, json=post , timeout=30)

    return responce.status_code

