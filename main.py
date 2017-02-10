#!/usr/bin/python
# coding:utf-8

from flask import Flask, jsonify, request
# from flask_restful import reqparse, abort, Api, Resource

from BS4Ins import BS4Ins
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return get_tasks('instagram')


@app.route('/api/images/<username>', methods=['GET'])
def get_tasks(username):
    last_id = request.args.get('id', '')
    data = BS4Ins().find_src_by_data('https://www.instagram.com/' + username + '/?max_id=' + last_id)
    return jsonify([ob.__dict__ for ob in data])


if __name__ == '__main__':
    app.run(debug=False)
