# coding=utf-8
from flask import Flask, request, jsonify, render_template
import urllib
import base64
import json
import requests
import apikeys
from cloud_vision_api import *
from image_cropper import *

app = Flask(__name__)
@app.route('/', methods=['GET'])
def hello ():
    return render_template('index.html')


@app.route('/api/v0/gyazo', methods=['POST'])
def gyazo ():
    # Upload with Browser Session API
    dic = request.json
    dic['client_id'] = apikeys.GYAZO_CLIENT_ID
    api_url = 'https://upload.gyazo.com/api/upload/easy_auth'
    params = urllib.urlencode(dic)
    f = urllib.urlopen(api_url, params)
    res = json.loads(f.read())
    gyazo_image = res['get_image_url']
    return jsonify({'get_image_url': gyazo_image})


@app.route('/api/v0/detect', methods=['POST'])
def detect ():
    got_json = request.json
    if ('image' in got_json):
        image_base64_str = got_json['image']
        img_jpg = image_base64_str.decode('base64')
        image_content = base64.b64encode(img_jpg)
        res_json = goog_cloud_vision_text(image_content)
        if len(res_json['responses']) > 0:
            res = res_json['responses'][0]
            if len(res['textAnnotations']) > 0:
                all_text = res['textAnnotations'][0]['description']
                keyword_positions = find_keywords(all_text, res['textAnnotations'])
                res_base64img = trim_image(image_base64_str, keyword_positions)
                res_json['base64image'] = 'data:image/jpeg;base64,' + res_base64img;

        res_json['description'] = 'Orange (Beta)'
        res_json['responses'] = [];
        return jsonify(res_json)
    else:
        return jsonify(description='Bad request')

app.run(port=8080, debug=True)
