# -*- coding: utf-8 -*-

from app import app, db
from app.models import Task
from flask import request, jsonify
from uuid import uuid4
import hashlib


@app.route('/submit', methods=['POST'])
def submit():
    id = str(uuid4())

    if request.form.get('email') is not None:
        email = request.form['email']
    else:
        email = None
    
    url = request.form['url']

    task = Task(id=id, url=url, status='running')
    db.session.add(task)
    db.session.commit()

    return id, 201


@app.route('/check', methods=['GET'])
def check():
    id = request.args['id']
    task = Task.query.get(id)
    if task is None:
        return f'{{"status":"not exist"}}', 404
    elif task.status == 'done':
        return f'{{"md5":{task.md5},"status":{task.status},"url":{task.url}}}',\
               200
    elif task.status == 'running':
        return f'{{"status":"{task.status}"}}', 202
    else:
        return f'{{"status":"{task.status}"}}', 400


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()