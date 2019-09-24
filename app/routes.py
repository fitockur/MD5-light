# -*- coding: utf-8 -*-

from app import app, db, mail
from app.models import Task
from flask import request, jsonify
from flask_mail import Message
from uuid import uuid4
from threading import Thread
import hashlib
import requests

def perform(cur_app, task_id, url, email):
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
                msg = Message('MD5Light', sender=cur_app.config['MAIL_USERNAME'],
                              recipients=[email])
                msg.body = f"url: {url}\nmd5: {md5}"
                with cur_app.app_context():
                    mail.send(msg)
        else:
            status = f'error: status code is {response.status_code}'

    task = Task.query.get(task_id)
    task.md5 = md5
    task.status = status
    db.session.commit()


@app.route('/submit', methods=['POST'])
def submit():
    id = str(uuid4()) # create task id

    if request.form.get('email') is not None:
        email = request.form['email']
    else:
        email = None
    
    url = request.form['url']
    
    """add to db"""
    task = Task(id=id, url=url, status='running')
    db.session.add(task)
    db.session.commit()

    """create new thread to send the task to work in the background"""
    Thread(target=perform, args=(app, id, url, email)).start()

    return jsonify({"id": id}), 201


@app.route('/check', methods=['GET'])
def check():
    id = request.args['id']
    task = Task.query.get(id) # None if doesn't exist

    if task is None:
        return jsonify({"status":"not exist"}), 404
    elif task.status == 'done':
        return jsonify({
            "md5": task.md5,
            "status": task.status,
            "url": task.url
            }), 200
    elif task.status == 'running':
        return jsonify({'status': task.status}), 202
    else:
        """code or description"""
        return jsonify({'status': task.status}), 400