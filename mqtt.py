import paho.mqtt.client as mqtt
import threading
from datetime import datetime
import pymysql
import json

class Mqtt(threading.Thread):
    def __init__(self, host, port, onConnect, onMessage):
        super(Mqtt, self).__init__()
        self.client = mqtt.Client('subscribe')
        self.client.on_connect = onConnect
        self.client.on_message = onMessage

        self.client.connect(host, port, 60)

    def run(self):
        self.client.loop_forever()

with open('config.json') as fp:
    config = json.loads(fp.read())

def onConnect(client, userdata, flags, rc):
    sub = ['photon/data']
    for s in sub:
        client.subscribe(s)
    print('Connected')

def onMessage(client, userdata, msg):
    payload = msg.payload.decode('utf-8').strip().split(' ')
    conn = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['passwd'],
        db='idb', charset='utf8'
    )
    cur = conn.cursor()
    now = datetime.now()
    for i in range(len(payload)//2):
        sql = 'INSERT INTO data VALUES(\"{}\", {}, \"{}\")'.format(payload[2*i], payload[2*i+1], now)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

client = Mqtt('localhost', 4000, onConnect, onMessage)
client.start()
