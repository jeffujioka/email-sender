import redis
import json
from time import sleep
from random import randint

if __name__ == "__main__":
    r = redis.Redis(host='queue', port=6379, db=0)
    while True:
        # msg = {'subject': 'Jefferson'}
        msg = json.loads(r.blpop('sender')[1])
        print('Sending message: ')
        print(msg)
        sleep(randint(5, 30))
        print('Message: ', msg['subject'], ' has been sent!')
