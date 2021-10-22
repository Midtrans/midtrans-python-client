import datetime

USED_SERVER_KEY='YOUR_SERVER_KEY'
USED_CLIENT_KEY='YOUR_CLIENT_KEY'

REUSED_ORDER_ID = [
    "py-midtransclient-test1-"+str(datetime.datetime.now()).replace(" ", "").replace(":", ""),
    "py-midtransclient-test2-"+str(datetime.datetime.now()).replace(" ", "").replace(":", ""),
    "py-midtransclient-test3-"+str(datetime.datetime.now()).replace(" ", "").replace(":", ""),
]

CC_TOKEN = ''
SAVED_CC_TOKEN = ''
API_RESPONSE = ''