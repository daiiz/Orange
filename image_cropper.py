# coding=utf-8
from PIL import Image
from io import BytesIO
import cStringIO
import base64
import math

KEYWORD_LEFT_TOP = u'左上'
KEYWORD_RIGHT_BOTTOM = u'右下'

# OCRによってキーワードが検出されているか
# 検出されていたならば座標情報を返す
def find_keywords (textBlock, text_annotations):
    positions = {
        'left_top': [],
        'right_bottom': []
    }
    a = KEYWORD_LEFT_TOP in textBlock
    b = KEYWORD_RIGHT_BOTTOM in textBlock
    toks = textBlock.split('\n')

    if a or b:
        for word_obj in text_annotations:
            tok = word_obj['description'].strip()
            if (tok == KEYWORD_LEFT_TOP):
                positions['left_top'] = word_obj['boundingPoly']['vertices']
            if (tok == KEYWORD_RIGHT_BOTTOM):
                positions['right_bottom'] = word_obj['boundingPoly']['vertices']

        # ひとまず，キャンバスの傾きは無視
        if len(positions['left_top']) > 0:
            h = (positions['left_top'][2]['y'] - positions['left_top'][1]['y'])
            lt = [positions['left_top'][2]['x'], positions['left_top'][2]['y'] + (h / 2)]
            x1 = positions['left_top'][1]['x']
            y1 = positions['left_top'][1]['y']
            x0 = positions['left_top'][0]['x']
            y0 = positions['left_top'][0]['y']
            deg = calcDegree(x1, y1, x0, y0)

            positions['left_top'] = lt
            positions['rotate_degree'] = deg
        if len(positions['right_bottom']) > 0:
            h = (positions['right_bottom'][2]['y'] - positions['right_bottom'][1]['y'])
            rb = [positions['right_bottom'][0]['x'], positions['right_bottom'][0]['y'] - (h / 2)]
            positions['right_bottom'] = rb

    return positions


# 2点がなす直線の水平角度を求める
def calcDegree (x2, y2, x1=0, y1=0):
    rad = math.atan2(y2 - y1, x2 - x1)
    deg = (rad * 180) / math.pi
    return deg


def trim_image (raw_image, pos_lt_rb):
    #deg = pos_lt_rb['rotate_degree']
    img = Image.open(BytesIO(base64.b64decode(raw_image)))
    # img = img.rotate(-1.0 * deg)
    width, height = img.size
    lt = [0, 0]
    rb = [width, height]

    if len(pos_lt_rb['left_top']) > 0:
        lt = pos_lt_rb['left_top']

    if len(pos_lt_rb['right_bottom']) > 0:
        rb = pos_lt_rb['right_bottom']

    w = abs(rb[0] - lt[0])
    h = abs(rb[1] - lt[1])
    #print(lt, rb, w, h)

    res_image = img.crop((lt[0], lt[1], rb[0], rb[1]))
    #print(res_image)

    buffer = cStringIO.StringIO()
    res_image.save(buffer, format="JPEG")
    base64img = base64.b64encode(buffer.getvalue())

    return base64img


if __name__ == '__main__':
    pass
