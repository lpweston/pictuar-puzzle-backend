from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from flask_cors import CORS
from utils.randomiser import randomiser
from utils.cropper import cropper
from datetime import datetime

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Image, PieceBeginner, Tile, PieceIntermediate, PieceHard, Game
    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def api():
        endpoints=open("endpoints.json","r")
        return endpoints.read()

    @app.route('/images/', methods=['POST', 'GET'])
    def images_handler():
        if request.method == "POST":
            url = str(request.data.get('url', ''))
            if url:
                image = Image(url=url)
                image.save()
                pieces = cropper(4, url)
                for item in pieces:
                    piece = PieceBeginner(img_id = image.id, value = item['value'], url=item['url'])
                    piece.save()
                beginner_pieces = PieceBeginner.query.filter_by(img_id=image.id)
                bpieces = []
                for piece in beginner_pieces:
                    obj = {
                        'value': piece.value,
                        'url': piece.url
                    }
                    bpieces.append(obj)
                response = jsonify({
                    'id': image.id,
                    'url': image.url,
                    'date_created': image.date_created,
                    'date_modified': image.date_modified,
                    'beginner_pieces': bpieces,
                })
                response.status_code = 201
                return response
        else:
            # GET
            images = Image.get_all()
            results = []
            for image in images:
                obj = {
                    'id': image.id,
                    'url': image.url,
                    'date_created': image.date_created,
                    'date_modified': image.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/images/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def image_manipulation(id, **kwargs):
         # retrieve a image using it's ID
        image = Image.query.filter_by(id=id).first()
        if not image:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            image.delete()
            return {
            "message": "image {} deleted successfully".format(image.id) 
         }, 200
        elif request.method == 'PUT':
            url = str(request.data.get('url', ''))
            image.url = url
            image.save()
            response = jsonify({
                'id': image.id,
                'url': image.url,
                'date_created': image.date_created,
                'date_modified': image.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            beginner_pieces = PieceBeginner.query.filter_by(img_id=id)
            bpieces = []
            for piece in beginner_pieces:
                obj = {
                    'value': piece.value,
                    'url': piece.url
                }
                bpieces.append(obj)
            intermediate_pieces = PieceIntermediate.query.filter_by(img_id=id)
            ipieces = []
            for piece in intermediate_pieces:
                obj = {
                    'value': piece.value,
                    'url': piece.url
                }
                ipieces.append(obj)
            hard_pieces = PieceHard.query.filter_by(img_id=id)
            hpieces = []
            for piece in hard_pieces:
                obj = {
                    'value': piece.value,
                    'url': piece.url
                }
                hpieces.append(obj)
            response = jsonify({
                'id': image.id,
                'url': image.url,
                'beginner_pieces': bpieces,
                'intermediate_pieces': ipieces,
                'hard_pieces': hpieces,
                'date_created': image.date_created,
                'date_modified': image.date_modified
            })
            response.status_code = 200
            return response

    @app.route('/images/<int:id>/intermediate-pieces', methods=['POST'])
    def add_intermediate_pieces(id, **kwargs):
     # retrieve a image using it's ID
        image = Image.query.filter_by(id=id).first()
        if not image:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        elif request.method == 'POST':
            value = str(request.data.get('value', ''))
            url = str(request.data.get('url', ''))
            piece = PieceIntermediate(img_id = id, value = value, url=url)
            piece.save()
            response = jsonify({
                'id': piece.id,
                'img_id': piece.img_id,
                'value': piece.value,
                'url': piece.url,
            })
            response.status_code = 201
            return response
    
    @app.route('/images/<int:id>/hard-pieces', methods=['POST'])
    def add_hard_pieces(id, **kwargs):
     # retrieve a image using it's ID
        image = Image.query.filter_by(id=id).first()
        if not image:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        elif request.method == 'POST':
            value = str(request.data.get('value', ''))
            url = str(request.data.get('url', ''))
            piece = PieceHard(img_id = id, value = value, url=url)
            piece.save()
            response = jsonify({
                'id': piece.id,
                'img_id': piece.img_id,
                'value': piece.value,
                'url': piece.url,
            })
            response.status_code = 201
            return response
            
    @app.route('/tiles/', methods=['POST', 'GET', 'PUT'])
    def tiles_handler():
        if request.method == "POST":
            url = str(request.data.get('url', ''))
            if url:
                tile = Tile(url=url)
                tile.save()
                response = jsonify({
                    'id': tile.id,
                    'url': tile.url
                })
                response.status_code = 201
                return response
        elif request.method == "PUT":
            id = str(request.data.get('id', ''))
            url = str(request.data.get('url',''))
            if url and id:
                tile =  Tile.query.filter_by(id=id).first()
                tile.url = url
                tile.save()
                response = jsonify({
                'id': tile.id,
                'url': tile.url
                })
                response.status_code = 200
                return response
        else:
            # GET
            tiles = Tile.get_all()
            results = []
            for tile in tiles:
                obj = {
                    'id': tile.id,
                    'url': tile.url
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/games/', methods=['POST', 'GET'])
    def game_handler():
        if request.method == "POST":
            img_id = str(request.data.get('img_id', ''))
            if img_id:
                obj = randomiser(4)
                one = obj[0]
                two = obj[1]
                three = obj[2]
                four = obj[3]
                win_img = obj['url']
                game = Game(img_id, one, two, three, four, win_img)
                game.save()
                score = 'null'
                response = jsonify({
                    'id': game.id,
                    'img_id': game.img_id,
                    'date_created': game.date_created,
                    'date_completed': game.date_completed,
                    'score': 'null',
                    'relation':{
                        '1': game.one,
                        '2' : game.two,
                        '3': game.three,
                        '4': game.four,
                    },
                    'win_img': game.win_img
                })
                response.status_code = 201
                return response
        else:
            # GET
            games = Game.get_all()
            results = []
            for game in games:
                if game.score:
                    score = game.score.strftime("%H:%M:%S")
                else:
                    score = 'null'
                obj = {
                    'id': game.id,
                    'img_id': game.img_id,
                    'date_created': game.date_created,
                    'date_completed': game.date_completed,
                    'score': score,
                    'relation':{
                        '1': game.one,
                        '2' : game.two,
                        '3': game.three,
                        '4': game.four,
                    },
                    'win_img': game.win_img
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/games/<int:id>', methods=['PUT', 'GET'])
    def game_complete(id, **kwargs):
        if request.method == "PUT":
            game =  Game.query.filter_by(id=id).first()
            game.score = datetime.now() - game.date_created
            game.save()
            score = game.score.strftime("%H:%M:%S")
            response = jsonify({
                'id': game.id,
                'img_id': game.img_id,
                'date_created': game.date_created,
                'date_completed': game.date_completed,
                'score': score,
                'relation':{
                    '1': game.one,
                    '2' : game.two,
                    '3': game.three,
                    '4': game.four,
                },
                'win_img': game.win_img
            })
            response.status_code = 200
            return response
        else:
            game =  Game.query.filter_by(id=id).first()
            if game.score:
                score = game.score.strftime("%H:%M:%S")
            else:
                score = 'null'
            response = jsonify({
                'id': game.id,
                'img_id': game.img_id,
                'date_created': game.date_created,
                'date_completed': game.date_completed,
                'score':score,
                'relation':{
                    '1': game.one,
                    '2' : game.two,
                    '3': game.three,
                    '4': game.four,
                },
                'win_img': game.win_img
            })
            response.status_code = 200
            return response

    return app