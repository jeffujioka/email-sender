import redis
import json
import os
from time import sleep
from random import randint

if __name__ == "__main__":
    redis_host = os.getenv('ENV_ESENDER_REDIS_HOSTNAME', 'queue')
    redis_port = int(os.getenv('ENV_ESENDER_REDIS_PORT', 6379))
    r = redis.Redis(host=redis_host, port=redis_port, db=0)
    print('Waiting for messages...')
    while True:
        # msg = {'subject': 'Jefferson'}
        msg = json.loads(r.blpop('sender')[1])
        print('Sending message: ')
        print(msg)
        sleep(randint(5, 30))
        print('Message: ', msg['subject'], ' has been sent!')
