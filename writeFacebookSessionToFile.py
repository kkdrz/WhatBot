import json

from fbchat import Client
from fbchat.models import *

client = Client('username', 'password')

session_cookies = client.getSession()

json = json.dumps(session_cookies)
f = open("session.json","w")
f.write(json)
f.close()