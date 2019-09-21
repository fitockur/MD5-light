# -*- coding: utf-8 -*-

from app import app
from flask import request

import random

queries = []


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_data().decode("utf-8")
    ddata = {}
    for elem in data.split('&'):
        pair = elem.split('=')
        ddata.update({pair[0]: pair[1]})
    ddata['id'] = str(random.randint(0, 100))
    ddata['status'] = 'running'
    queries.append(ddata)
    return queries[-1]['id'], 201


@app.route('/check', methods=['GET'])
def check():
    idx = request.args
    return idx, 200