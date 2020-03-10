import json

from datetime import datetime, timedelta
from fbchat import Client, log
from fbchat.models import *

lastMessageTime = {}

class WhatBot(Client):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        now = datetime.now()

        lastMessageTime[author_id]=now
        lastMessageTime[thread_id]=now


    def onTyping(self, author_id=None, status=None, thread_id=None, thread_type=None, msg=None):
        
        now = datetime.now()

        if thread_type == ThreadType.GROUP:
            return

        if author_id in lastMessageTime:
            
            lastMessageFromAuthor = lastMessageTime[author_id]

            someTimeAgo = now - timedelta(minutes=15)

            if lastMessageFromAuthor < someTimeAgo :
                self.send(Message(text='co tam? :)'), thread_id=thread_id, thread_type=thread_type)

        else:
            self.send(Message(text='co tam? :)'), thread_id=thread_id, thread_type=thread_type)
        
        lastMessageTime[author_id] = now


with open('session.json') as json_file:
    data = json.load(json_file)

client = WhatBot('', '', session_cookies=data)
client.listen()


