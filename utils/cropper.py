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
    whole_rs = whole.resize((400,400))
    beginner_pieces = [
        whole_rs.crop((0,0,200,200)),
        whole_rs.crop((200,0,400,200)),
        whole_rs.crop((0,200,200,400)),
        whole_rs.crop((200,200,400,400))
    ]
    assignment = []
    n=0
    for piece in beginner_pieces:
        n = n + 1
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
            assignment.append({'value':n , 'url': res['data']['link']})

    return assignment