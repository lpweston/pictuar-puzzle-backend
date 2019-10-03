# PictuAR Puzzle Back End

## Introdution

This is the back end api for the AR game [PictuAR Puzzle](https://github.com/lpweston/pictuar-puzzle).

Written in python 3 and using Flask, SQLAlchemy and Postgres.

## Installing

Clone and change into the directory

```
git clone https://github.com/lpweston/pictuar-puzzle-backend
cd pictuar-puzzle-backend
```

Add a .env containing the following

```
source venv/bin/activate
export FLASK_APP="run.py"
export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
export APP_SETTINGS="development"
export DATABASE_URL="postgresql://[PostGres_username]:[PostGres_Password]@localhost/flask_api"
```

Where [PostGres_username] and [PostGres_Password] are replaced.

And and /instance/config.pg, with the same replacement.

```
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://[PostGres_username]:[PostGres_Password]@localhost/flask_api"
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
```
