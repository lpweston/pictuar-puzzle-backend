# PictuAR Puzzle Back End

## Introdution

This is the back end api for the AR game [PictuAR Puzzle](https://github.com/lpweston/pictuar-puzzle).

Written in python 3 and using Flask, SQLAlchemy and Postgres.

## Installing

### Requirements

Python 3,
Virtualenv

### Installing

Clone and change into the directory

```
git clone https://github.com/lpweston/pictuar-puzzle-backend
cd pictuar-puzzle-backend
```

set up your virtual environment

```
virtualenv  venv
```

Add a .env containing the following

```
source venv/bin/activate
export FLASK_APP="run.py"
export SECRET="some-very-long-string-of-random-characters-and-a-bottle-of-rum"
export APP_SETTINGS="development"
export DATABASE_URL="postgresql://[PostGres_username]:[PostGres_Password]@localhost/flask_api"
export TEST_DB="postgresql://[PostGres_username]:[PostGres_Password]@localhost/test_db"
```

Install and set up autoenv

```
pip install -r requirements.txt
pip install autoenv
echo "source `which activate.sh`" >> ~/.bashrc
$ source ~/.bashrc
```

You should be asked to approve it the first time, but if not try typing

```
source .env
```

You're looking for it to say venv

Install required dependencies

```
pip install -r requirements.txt
```

Where [PostGres_username] and [PostGres_Password] are replaced.
