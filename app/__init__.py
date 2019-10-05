from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Image, PieceBeginner, Tile
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def api():
        endpoints=open("endpoints.json","r")
        return endpoints.read()

    @app.route('/images/', methods=['POST', 'GET'])
    def images():
        if request.method == "POST":
            url = str(request.data.get('url', ''))
            if url:
                image = Image(url=url)
                image.save()
                response = jsonify({
                    'id': image.id,
                    'url': image.url,
                    'date_created': image.date_created,
                    'date_modified': image.date_modified
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
            pieces = []
            for piece in beginner_pieces:
                obj = {
                    'value': piece.value,
                    'url': piece.url
                }
                pieces.append(obj)
            response = jsonify({
                'id': image.id,
                'url': image.url,
                'beginner_pieces': pieces,
                'date_created': image.date_created,
                'date_modified': image.date_modified
            })
            response.status_code = 200
            return response
    
    @app.route('/images/<int:id>/beginner-pieces', methods=['POST'])
    def add_beginner_pieces(id, **kwargs):
     # retrieve a image using it's ID
        image = Image.query.filter_by(id=id).first()
        if not image:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        elif request.method == 'POST':
            value = str(request.data.get('value', ''))
            url = str(request.data.get('url', ''))
            piece = PieceBeginner(img_id = id, value = value, url=url)
            piece.save()
            response = jsonify({
                'id': piece.id,
                'img_id': piece.img_id,
                'value': piece.value,
                'url': piece.url,
            })
            response.status_code = 201
            return response
            
    @app.route('/tiles/', methods=['POST', 'GET'])
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
        else:
            # GET
            tiles = Tile.get_all()
            print(tiles)
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

    return app