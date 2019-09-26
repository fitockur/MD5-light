from app import db, mail
from .models import Task
from flask_mail import Message
import requests
import hashlib

def perform(app, task_id, url, email):
    md5 = None
    hash = hashlib.md5()

    try:
        response = requests.get(url, timeout=10) # get file content
    except requests.RequestException:
        status = 'error: bad request'
    else:
        if response.status_code == 200: # code 200 is OK
            for chunk in response.iter_content(chunk_size=4096): # if file is large
                hash.update(chunk)
            md5 = hash.hexdigest()
            status = 'done'

            if email: # optional
                send_email(app=app, email=email, subject='MD5Light',
                           sender=app.config['MAIL_USERNAME'],
                           text=f"url: {url}\nmd5: {md5}")
        else:
            status = f'error: status code is {response.status_code}'

    task = Task.query.get(task_id)
    task.md5 = md5
    task.status = status
    db.session.commit()


def send_email(app, email, subject, sender, text):
    msg = Message(subject=subject, sender=sender, recipients=[email])
    msg.body = text
    with app.app_context():
        mail.send(msg)