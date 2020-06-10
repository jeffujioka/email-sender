from bottle import route, run, request

@route('/', method='POST')
def send():
    subject = request.forms.get('subject')
    msg = request.forms.get('message')
    return f'Message has been queued!\nSubject: {subject}\nMessage: {msg}'

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
