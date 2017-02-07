# coding=utf-8
import json
import requests
import apikeys

GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='

# Google Cloud Vision API を呼ぶ
def goog_cloud_vision (image_content, task_name='LABEL_DETECTION'):
    api_url = GOOGLE_CLOUD_VISION_API_URL + apikeys.CLOUD_VISION
    req_body = json.dumps({
        'requests': [{
            'image': {
                'content': image_content
            },
            'features': [{
                'type': task_name,
                'maxResults': 10,
            }]
        }]
    })

    res = requests.post(api_url, data=req_body)
    return res.json()


def goog_cloud_vision_text (image_content):
    return goog_cloud_vision(image_content, 'TEXT_DETECTION')
