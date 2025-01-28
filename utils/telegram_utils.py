import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def copyMessages(start, end, from_chat, to_chat):
    url = BASE_API_URL + "copyMessages"
    print(start, end, list(range(start, end + 1)))
    payload = {
        "from_chat_id": from_chat,
        "chat_id": to_chat,
        "message_ids": json.dumps(list(range(start, end + 1))),
    }
    resp = requests.post(url, params=payload)
    print(resp.text)

def copyMessage(message_id, from_chat, to_chat, keyboard):
    url = BASE_API_URL + "copyMessage"
    payload = {
        "from_chat_id": from_chat,
        "chat_id": to_chat,
        "message_id": message_id,
        "reply_markup": json.dumps(keyboard),
    }
    resp = requests.post(url, params=payload)
    print(resp.text)

def sendKeyboard(chat_id, response, keyboard):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": response,
        "reply_markup": json.dumps(keyboard),
    }
    res = requests.post(url=url, json=payload)
    print(res.text)

def sendMessage(response, chat_id, parse=False):
    url = BASE_API_URL + "sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": response,
    }
    if parse:
        payload["parse_mode"] = "MarkdownV2"
    response = requests.post(url, json=payload)
    print(response.text)

def sendVideo(file_id, chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    payload = {"chat_id": chat_id, "video": file_id}
    resp = requests.post(url=url, json=payload)
    print(resp.text)

def sendDocument(chat_id, document, caption=None, parse_mode=None, disable_notification=False, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    payload = {
        "chat_id": chat_id,
        "document": document,
        "disable_notification": disable_notification,
    }
    if caption:
        payload["caption"] = caption
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    response = requests.post(url, json=payload)
    print(response.text)
