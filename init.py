import os
import json

path = os.path.dirname(os.path.realpath(__file__))

with open(path + '/config.json') as fp:
    config = json.loads(fp.read())

os.system('python3 -m virtualenv {}/.env'.format(path))
os.system('{path}/.env/bin/pip install -r {path}/requirements.txt'.format(path=path))
os.system('mysql -u{} -p{} -e "source init.sql"'.format(config['user'], config['passwd']))
