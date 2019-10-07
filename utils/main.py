from PIL import Image
import random

tiles = [
    Image.open('./c1.png'), 
    Image.open('./c2.png'), 
    Image.open('./c3.png'), 
    Image.open('./c4.png')
    ]

random.shuffle(tiles)

whole = Image.new('RGBA',(400,400),'white')

whole.paste(tiles[0].resize((200,200)),(0,0))
whole.paste(tiles[1].resize((200,200)),(200,0))
whole.paste(tiles[2].resize((200,200)),(0,200))
whole.paste(tiles[3].resize((200,200)),(200,200))

whole.save('./whole.png')