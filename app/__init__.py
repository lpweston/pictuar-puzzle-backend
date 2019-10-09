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
    from app.models import Image, PieceBeginner, Tile, PieceIntermediate, PieceHard, Game, User
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

    @app.route('/users/', methods=['POST', 'GET'])
    def users_handler():
        if request.method == "POST":
            username = str(request.data.get('username', ''))
            email = str(request.data.get('email', ''))
            name = str(request.data.get('name', ''))
            password = str(request.data.get('password', ''))
            if username and email and password:
                user = User(email, username, name, password)
                user.save()
                response = jsonify({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'password': user.password
                })
                response.status_code = 201
                return response
        else:
            # GET
            users = User.get_all()
            results = []
            for user in users:
                obj = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': user.name,
                    'password': user.password
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    @app.route('/users/<int:id>', methods=['GET'])
    def user_handler(id, **kwargs):
        user = User.query.filter_by(id=id).first()
        result = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'password': user.password
        }
        response = jsonify(result)
        response.status_code = 200
        return response

    @app.route('/images/', methods=['POST', 'GET'])
    def images_handler():
        if request.method == "POST":
            url = str(request.data.get('url', ''))
            diff = int(request.data.get('diff', ''))
            user_id = int(request.data.get('user_id', ''))
            if url and diff:
                image = Image(url, user_id)
                image.save()
                pieces = cropper(diff, url)
                if diff == 4:
                    for item in pieces:
                        piece = PieceBeginner(img_id = image.id, value = item['value'], url=item['url'])
                        piece.save()
                if diff == 9:
                    for item in pieces:
                        piece = PieceIntermediate(img_id = image.id, value = item['value'], url=item['url'])
                        piece.save()
                if diff == 16:
                    for item in pieces:
                        piece = PieceHard(img_id = image.id, value = item['value'], url=item['url'])
                        piece.save()
                beginner_pieces = PieceBeginner.query.filter_by(img_id=image.id)
                bpieces = []
                for piece in beginner_pieces:
                    obj = {
                        'value': piece.value,
                        'url': piece.url
                    }
                    bpieces.append(obj)
                intermediate_pieces = PieceIntermediate.query.filter_by(img_id=image.id)
                ipieces = []
                for piece in intermediate_pieces:
                    obj = {
                        'value': piece.value,
                        'url': piece.url
                    }
                    ipieces.append(obj)
                hard_pieces = PieceHard.query.filter_by(img_id=image.id)
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
                    'user_id': image.user_id,
                    'date_created': image.date_created,
                    'date_modified': image.date_modified,
                    'beginner_pieces': bpieces,
                    'intermediate_pieces': ipieces,
                    'hard_pieces': hpieces
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
                    'date_modified': image.date_modified,
                    'user_id': image.user_id
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
                'user_id': image.user_id,
                'date_created': image.date_created,
                'date_modified': image.date_modified
            })
            response.status_code = 200
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
            diff = int(request.data.get('diff', ''))
            user_id = int(request.data.get('user_id', ''))
            if img_id and diff:
                obj = randomiser(diff)
                rel = []
                for num in range(0,diff):
                    num = num +1 
                    rel.append(obj[num-1])
                win_img = obj['url']
                game = Game(img_id, rel, win_img, user_id)
                game.save()
                relation = {}
                if game.t1:
                    relation['1'] = game.t1
                if game.t2:
                    relation['2'] = game.t2
                if game.t3:
                    relation['3'] = game.t3
                if game.t4:
                    relation['4'] = game.t4
                if game.t5:
                    relation['5'] = game.t5
                if game.t6:
                    relation['6'] = game.t6
                if game.t7:
                    relation['7'] = game.t7
                if game.t8:
                    relation['8'] = game.t8
                if game.t9:
                    relation['9'] = game.t9
                if game.t10:
                    relation['10'] = game.t10
                if game.t11:
                    relation['11'] = game.t11
                if game.t12:
                    relation['12'] = game.t12
                if game.t13:
                    relation['13'] = game.t13
                if game.t14:
                    relation['14'] = game.t14
                if game.t15:
                    relation['15'] = game.t15
                if game.t16:
                    relation['16'] = game.t16
                score = 'null'
                response = jsonify({
                    'id': game.id,
                    'img_id': game.img_id,
                    'user_id': game.user_id,
                    'date_created': game.date_created,
                    'date_completed': game.date_completed,
                    'score': 'null',
                    'relation':relation,
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
                relation = {}
                if game.t1:
                    relation['1'] = game.t1
                if game.t2:
                    relation['2'] = game.t2
                if game.t3:
                    relation['3'] = game.t3
                if game.t4:
                    relation['4'] = game.t4
                if game.t5:
                    relation['5'] = game.t5
                if game.t6:
                    relation['6'] = game.t6
                if game.t7:
                    relation['7'] = game.t7
                if game.t8:
                    relation['8'] = game.t8
                if game.t9:
                    relation['9'] = game.t9
                if game.t10:
                    relation['10'] = game.t10
                if game.t11:
                    relation['11'] = game.t11
                if game.t12:
                    relation['12'] = game.t12
                if game.t13:
                    relation['13'] = game.t13
                if game.t14:
                    relation['14'] = game.t14
                if game.t15:
                    relation['15'] = game.t15
                if game.t16:
                    relation['16'] = game.t16
                obj = {
                    'id': game.id,
                    'img_id': game.img_id,
                    'date_created': game.date_created,
                    'date_completed': game.date_completed,
                    'score': score,
                    'user_id': game.user_id,
                    'relation':relation,
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
            relation = {}
            if game.t1:
                relation['1'] = game.t1
            if game.t2:
                relation['2'] = game.t2
            if game.t3:
                relation['3'] = game.t3
            if game.t4:
                relation['4'] = game.t4
            if game.t5:
                relation['5'] = game.t5
            if game.t6:
                relation['6'] = game.t6
            if game.t7:
                relation['7'] = game.t7
            if game.t8:
                relation['8'] = game.t8
            if game.t9:
                relation['9'] = game.t9
            if game.t10:
                relation['10'] = game.t10
            if game.t11:
                relation['11'] = game.t11
            if game.t12:
                relation['12'] = game.t12
            if game.t13:
                relation['13'] = game.t13
            if game.t14:
                relation['14'] = game.t14
            if game.t15:
                relation['15'] = game.t15
            if game.t16:
                relation['16'] = game.t16
            response = jsonify({
                'id': game.id,
                'img_id': game.img_id,
                'date_created': game.date_created,
                'date_completed': game.date_completed,
                'score': score,
                'user_id': game.user_id,
                'relation':relation,
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
            relation = {}
            if game.t1:
                relation['1'] = game.t1
            if game.t2:
                relation['2'] = game.t2
            if game.t3:
                relation['3'] = game.t3
            if game.t4:
                relation['4'] = game.t4
            if game.t5:
                relation['5'] = game.t5
            if game.t6:
                relation['6'] = game.t6
            if game.t7:
                relation['7'] = game.t7
            if game.t8:
                relation['8'] = game.t8
            if game.t9:
                relation['9'] = game.t9
            if game.t10:
                relation['10'] = game.t10
            if game.t11:
                relation['11'] = game.t11
            if game.t12:
                relation['12'] = game.t12
            if game.t13:
                relation['13'] = game.t13
            if game.t14:
                relation['14'] = game.t14
            if game.t15:
                relation['15'] = game.t15
            if game.t16:
                relation['16'] = game.t16
            response = jsonify({
                'id': game.id,
                'img_id': game.img_id,
                'date_created': game.date_created,
                'date_completed': game.date_completed,
                'score': score,
                'relation': relation,
                'user_id': game.user_id,
                'win_img': game.win_img
            })
            response.status_code = 200
            return response

    return app