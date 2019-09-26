from app import app, db
from .models import Task
from .main import perform
from flask import request, jsonify
from uuid import uuid4
from threading import Thread


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