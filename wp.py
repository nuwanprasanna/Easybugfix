import requests
import json
import base64
from datetime import datetime
global url

url = "https://easybugfix.com/wp-json/wp/v2"
user = "Laura"
password = "aRwP qVMh V3fm c8RP 4x11 euNh"
credentials = user + ':' + password
token = base64.b64encode(credentials.encode())

def post(post):
    global url, token

    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    responce = requests.post(url + '/posts', headers=header, json=post , timeout=30)

    return responce.json()


def get_tags():
    global url, token

    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    responce = requests.get(url + '/tags', headers=header, timeout=30)
    responce = responce.json()

    x={ a['name']:a['id'] for a in responce}

    return x

def create_tag(tag):
    global url, token
        
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    responce = requests.post(url + '/tags', headers=header, json= { 'name': tag}, timeout=30)

    return responce.json()

def create_category(cat):
    global url, token
        
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    responce = requests.post(url + '/categories', headers=header, json= { 'name': cat.capitalize()}, timeout=30)

    return responce.json()
