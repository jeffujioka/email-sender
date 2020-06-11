import redis
import json
import os
import psycopg2
from bottle import Bottle, request


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        redis_host = os.getenv('ENV_ESENDER_REDIS_HOSTNAME', 'queue')
        redis_port = int(os.getenv('ENV_ESENDER_REDIS_PORT', 6379))

        print(f'ENV_ESENDER_REDIS_HOSTNAME={redis_host} -> ', type(redis_host))
        print(f'ENV_ESENDER_REDIS_PORT={redis_port} -> ', type(redis_port))
        self.queue = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

        db_hostname = os.getenv('ENV_ESENDER_DB_HOSTNAME', 'email-sender-db')
        db_name = os.getenv('ENV_ESENDER_DB_NAME', 'email_sender')
        user = os.getenv('ENV_ESENDER_DB_USER', 'postgres')
        password = os.getenv('ENV_ESENDER_DB_PASSWORD', 'postgres')
        
        print(f'ENV_ESENDER_DB_HOSTNAME={db_hostname}')
        print(f'ENV_ESENDER_DB_NAME={db_name}')
        print(f'ENV_ESENDER_DB_USER={user}')
        print(f'ENV_ESENDER_DB_PASSWORD={password}')

        DSN = f'dbname={db_name} user={user} password={password} host={db_hostname}'
        self.conn = psycopg2.connect(DSN)

    def register_message(self, subject, message):
        cur = self.conn.cursor()
        SQL = 'INSERT INTO emails (subject, message) VALUES (%s, %s)'
        cur.execute(SQL, (subject, message))
        self.conn.commit()
        cur.close()

        msg = {'subject': subject, 'message': message}
        self.queue.rpush('sender', json.dumps(msg))

        print('Message saved on database')

    def send(self):
        subject = request.forms.get('subject')
        msg = request.forms.get('message')

        self.register_message(subject, msg)

        return f'Message has been queued!\nSubject: {subject}\nMessage: {msg}'

if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)
