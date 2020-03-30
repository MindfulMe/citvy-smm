# AI transfer photo server 

You should install all requirements to run server

## Installation

Use the pipenv manager to install requirements.

```bash
pip install pipenv
pipenv --python 2.7.10 
pipenv install
sh ./setup.sh
```

## Usage

```python
export FLASK_APP=appfl.py
python2 -m flask run
```
Give to localhost:8000 photo and it return transfered photo to 1 of 6 styles (random choice default)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

# Telegram BOT

## Running Telegram BOT

```
python3 bot.py
```
The server is running and you can see `@citvy_photo_bot` in telegram