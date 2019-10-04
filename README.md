# PictuAR Puzzle Back End

## Introdution

This is the back end api for the AR game [PictuAR Puzzle](https://github.com/lpweston/pictuar-puzzle).

Written in python 3 and using Flask, SQLAlchemy and Postgres.

## Installing

### Requirements

Python 3,
Pip
Virtualenv

### Installing

Clone and change into the directory

```
git clone https://github.com/lpweston/pictuar-puzzle-backend
cd pictuar-puzzle-backend
```

set up your virtual environment

```
python3 -m venv venv
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

Where [PostGres_username] and [PostGres_Password] are replaced.

Install and set up autoenv

```
pip install -r requirements.txt
pip install autoenv
echo "source `which activate.sh`" >> ~/.bashrc
source ~/.bashrc
```

You should be asked to approve it the first time, but if not try typing

```
source .env
```

You're looking for it to say (venv) on the left of your file name and branch.

## Running

To run the server locally:

```
flask run
```

To run test suite:

```
python test_server.py
```
