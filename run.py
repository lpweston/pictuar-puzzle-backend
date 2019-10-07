import os
from flask_cors import CORS, cross_origin
from app import create_app

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = create_app(config_name)

if __name__ == '__main__':
    app.run()