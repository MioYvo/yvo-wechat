# coding=utf-8
# __author__ = 'Mio'
import logging

import requests
import itchat
from redis import Redis
from random import randint

API_URL = "http://www.tuling123.com/openapi/api"
API_KEY = "9315949fb0004946a9b2d749d6318661"
r = Redis()

GUESS_NUMBER_KEY = "GUESS_NUMBER_{}"


def bot_get_msg(info, user_id):
    res = requests.post(API_URL, json={"key": API_KEY, "info": info, "userid": user_id})
    data = res.json()
    text = data['text']
    url = data.get('url', '')
    return "{} {}".format(text, url)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_text_reply(msg):
    if msg.MsgType != 1 or not msg.isAt:
        return

    # text = msg.Content
    text = msg.text.split()[1]
    print("Group Chat ActualNickName: ", msg.ActualNickName)

    # guess number
    try:
        text = int(text)
    except Exception as e:
        logging.error(e)
        print("cannot transfer to int; continue")
        if text == "猜数字":
            reply_text = GuessNumber(name=msg.ActualNickName).guess()
        else:
            reply_text = bot_get_msg(text, user_id=msg.ActualNickName)
    else:
        reply_text = GuessNumber(name=msg.ActualNickName, guess_number=text).guess()

    reply_msg = "@{}\u2005{}".format(msg.ActualNickName, reply_text)
    itchat.send(msg=reply_msg, toUserName=msg.FromUserName)
    return


# @itchat.msg_register(INCOME_MSG)
@itchat.msg_register(itchat.content.TEXT)
def single_text_reply(msg):
    if msg.MsgType != 1:
        return

    text = msg.text
    print("Single Chat NickName: ", msg.User.NickName)

    # guess number
    try:
        text = int(text)
    except Exception as e:
        logging.error(e)
        print("cannot transfer to int; continue")
        if text == "猜数字":
            reply_text = GuessNumber(name=msg.User.NickName).guess()
        else:
            reply_text = bot_get_msg(text, user_id=msg.User.NickName)
    else:
        reply_text = GuessNumber(name=msg.User.NickName, guess_number=text).guess()

    itchat.send(msg=reply_text, toUserName=msg.FromUserName)


class GuessNumber(object):
    def __init__(self, name, guess_number=None):
        self.name = name
        self.guess_number = guess_number
        self.start_point = 1
        self.end_point = 100
        self.key = GUESS_NUMBER_KEY.format(self.name)

        self.update_start_end()

    def update_start_end(self):
        start, end = r.hget(self.key, 'start_point'), r.hget(self.key, 'end_point')
        if start and end:
            self.start_point, self.end_point = int(start), int(end)

    def start_guess_number(self):
        r.hset(self.key, 'name', self.name)
        r.hset(self.key, 'start_point', self.start_point)
        r.hset(self.key, 'end_point', self.end_point)
        r.hset(self.key, 'target_number', randint(self.start_point, self.end_point))
        r.hset(self.key, 'current_number', '')

    @property
    def target(self):
        t = r.hget(self.key, 'target_number')
        if t is None:
            self.start_guess_number()
            return self.target
        else:
            return int(t)

    def set_range(self, start, end):
        r.hset(self.key, 'start_point', start)
        r.hset(self.key, 'end_point', end)
        self.start_point, self.end_point = start, end

    def guess(self):
        if self.guess_number is not None:
            if self.guess_number > self.target:
                self.set_range(self.start_point, min(self.guess_number, self.end_point))
            elif self.guess_number < self.target:
                self.set_range(max(self.start_point, self.guess_number), self.end_point)
            else:
                r.delete(self.key)
                return "你赢了！数字是: {}".format(self.guess_number)

            return "范围 {} - {}".format(self.start_point, self.end_point)
        else:
            self.start_guess_number()
            return "开始猜数字啦：范围 {} - {}".format(self.start_point, self.end_point)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    # itchat.send('Hello, 小冰', toUserName=itchat.search_mps(name="小冰")[0].UserName)
    itchat.run()
