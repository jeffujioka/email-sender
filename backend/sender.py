import redis
import json
import psycopg2
from bottle import Bottle, request


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)
        self.queue = redis.StrictRedis(host='queue', port=6379, db=0)
        DSN = 'dbname=email_sender user=postgres password=postgres host=email-sender-db'
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
