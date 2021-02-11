# - coding: utf-8 --
from os import environ
from sys import exit

from src import create_app
from config import config_dict

get_config_mode = environ.get('CONFIG_MODE', 'Production')
try:
    config_mode = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid CONFIG_MODE environment variable entry.')

app = create_app(config_mode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6543)
