import os
import io
import requests
from PIL import Image
import tempfile
import json
import base64

def cropper(diff, url):
    if 'jpg' in url:
        url = url.replace('.jpg','.png')
    response = requests.get(url)
    whole = Image.open(io.BytesIO(response.content))
    whole_rs = whole.resize((600,600))
    if diff == 4:
        imgPieces = [
            whole_rs.crop((0,0,300,300)),
            whole_rs.crop((300,0,600,300)),
            whole_rs.crop((0,300,300,600)),
            whole_rs.crop((300,300,600,600))
        ]
    elif diff == 9:
        imgPieces = [
            whole_rs.crop((0,0,200,200)),
            whole_rs.crop((200,0,400,200)),
            whole_rs.crop((400,0,600,200)),
            whole_rs.crop((0,200,200,400)),
            whole_rs.crop((200,200,400,400)),
            whole_rs.crop((400,200,600,400)),
            whole_rs.crop((0,400,200,600)),
            whole_rs.crop((200,400,400,600)),
            whole_rs.crop((400,400,600,600)),
        ]
    elif diff == 16:
        imgPieces = [
            whole_rs.crop((0,0,150,150)),
            whole_rs.crop((150,0,300,150)),
            whole_rs.crop((300,0,450,150)),
            whole_rs.crop((450,0,600,150)),
            whole_rs.crop((0,150,150,300)),
            whole_rs.crop((150,150,300,300)),
            whole_rs.crop((300,150,450,300)),
            whole_rs.crop((450,150,600,300)),
            whole_rs.crop((0,300,150,450)),
            whole_rs.crop((150,300,300,450)),
            whole_rs.crop((300,300,450,450)),
            whole_rs.crop((450,300,600,450)),
            whole_rs.crop((0,450,150,600)),
            whole_rs.crop((150,450,300,600)),
            whole_rs.crop((300,450,450,600)),
            whole_rs.crop((450,450,600,600)),
        ]
    assignment = []
    num=0
    for piece in imgPieces:
        num = num + 1
        buffered = io.BytesIO()
        piece.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        payload = {'image': img_str}
        headers = {
            'Authorization': 'Bearer fc0a9f7020eae6353ae08011ef2852caff0e0922'
        }
        response = requests.request('POST', url='https://api.imgur.com/3/image', headers = headers, data = payload, allow_redirects=False)
        if response.status_code==200:
            res = json.loads(response.content.decode('utf-8'))
            assignment.append({'value':num , 'url': res['data']['link']})

    return assignment