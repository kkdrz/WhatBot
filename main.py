import json

import random
from datetime import datetime, timedelta
from fbchat import Client, log
from fbchat.models import *
import argparse

parser = argparse.ArgumentParser(description='WhatBot Facebook.')

parser.add_argument('--replyAfter', type=int, nargs='+', dest="replyAfter", default=8,
            help='time from the last message after which it will reply (hours)')
parser.add_argument('--responsesFile', dest="responsesFile", default='responses.json', help='JSON file with responses (it will choose random one)')
parser.add_argument('--sessionFile', dest="sessionFile", default='session.json', help='JSON file with Facebook session')

args = parser.parse_args()


class WhatBot(Client):

    lastMessageTime = {}

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        now = datetime.now()

        self.lastMessageTime[author_id]=now
        self.lastMessageTime[thread_id]=now

    def onTyping(self, author_id=None, status=None, thread_id=None, thread_type=None, msg=None):
        
        if self.shouldSendResponse(author_id, thread_type):
            self.send(Message(text=self.randomResponse(args.responsesFile)), thread_id=thread_id, thread_type=thread_type)
            self.lastMessageTime[author_id] = datetime.now()

    def shouldSendResponse(self, id, thread_type):
        if thread_type == ThreadType.GROUP:
            return False

        if id in self.lastMessageTime:
            lastMessageWithId = self.lastMessageTime[id]

            someTimeAgo = datetime.now() - timedelta(hours=args.replyAfter)

            return lastMessageWithId < someTimeAgo
        else:
            return True;

    def randomResponse(self, file):
        with open(file) as json_file:
            responses = json.load(json_file)
        return random.choice(responses)


with open(args.sessionFile) as session_file:
   session = json.load(session_file)

client = WhatBot('', '', session_cookies=session, logging_level=50)
client.listen()




    