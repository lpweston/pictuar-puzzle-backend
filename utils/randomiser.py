import os
import io
import requests
from PIL import Image
import tempfile
import random
import json
import base64

def randomiser(diff):
    from app.models import Tile
    assignment = {}
    images = {}
    tiles = Tile.get_all()
    tilesObj = []
    for tile in tiles:
        obj = {
                'id': tile.id,
                'url': tile.url
            }
        tilesObj.append(obj)

    whole = Image.new('RGBA',(600,600),'white')
    random.shuffle(tilesObj)

    for num in range(0,diff):
        tile = tilesObj[num]
        url = tile['url']
        imgid = tile['id']
        assignment[num] = imgid
        buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            downloaded = 0
            filesize = int(r.headers['content-length'])
            for chunk in r.iter_content():
                downloaded += len(chunk)
                buffer.write(chunk)
            buffer.seek(0)
            images[num] = Image.open(io.BytesIO(buffer.read()))
        buffer.close()
    
    if diff == 4:
        whole.paste(images[0].resize((300,300)),(0,0))
        whole.paste(images[1].resize((300,300)),(300,0))
        whole.paste(images[2].resize((300,300)),(0,300))
        whole.paste(images[3].resize((300,300)),(300,300))
    elif diff == 9:
        whole.paste(images[0].resize((200,200)),(0,0))
        whole.paste(images[1].resize((200,200)),(200,0))
        whole.paste(images[2].resize((200,200)),(400,0))
        whole.paste(images[3].resize((200,200)),(0,200))
        whole.paste(images[4].resize((200,200)),(200,200))
        whole.paste(images[5].resize((200,200)),(400,200))
        whole.paste(images[6].resize((200,200)),(0,400))
        whole.paste(images[7].resize((200,200)),(200,400))
        whole.paste(images[8].resize((200,200)),(400,400))
    elif diff == 16:
        whole.paste(images[0].resize((150,150)),(0,0))
        whole.paste(images[1].resize((150,150)),(150,0))
        whole.paste(images[2].resize((150,150)),(300,0))
        whole.paste(images[3].resize((150,150)),(450,0))
        whole.paste(images[4].resize((150,150)),(0,150))
        whole.paste(images[5].resize((150,150)),(150,150))
        whole.paste(images[6].resize((150,150)),(300,150))
        whole.paste(images[7].resize((150,150)),(450,150))
        whole.paste(images[8].resize((150,150)),(0,300))
        whole.paste(images[9].resize((150,150)),(150,300))
        whole.paste(images[10].resize((150,150)),(300,300))
        whole.paste(images[11].resize((150,150)),(450,300))
        whole.paste(images[12].resize((150,150)),(0,450))
        whole.paste(images[13].resize((150,150)),(150,450))
        whole.paste(images[14].resize((150,150)),(300,450))
        whole.paste(images[15].resize((150,150)),(450,450))

    buffered = io.BytesIO()
    whole.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())

    imgururl = 'https://api.imgur.com/3/image'
    payload = {'image': img_str}
    files = {}
    headers = {
    'Authorization': 'Bearer fc0a9f7020eae6353ae08011ef2852caff0e0922'
    }
    response = requests.request('POST', url='https://api.imgur.com/3/image', headers = headers, data = payload, files = files, allow_redirects=False)
    if response.status_code==200:
        res = json.loads(response.content.decode('utf-8'))
        assignment['url'] = res['data']['link']

    return assignment
