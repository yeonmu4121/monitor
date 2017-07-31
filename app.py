from flask import Flask, url_for, render_template, redirect
import json
import pymysql

app = Flask(__name__)
with open('config.json') as fp:
    config = json.loads(fp.read())

@app.route('/')
def index():
    return redirect(url_for('monitor'))

@app.route('/monitor')
def monitor():
    with open('table.json') as fp:
        table = json.loads(fp.read())
    return render_template('monitor.html', table=table, title=config['title'])

@app.route('/plot/<graph>/period/<int:period>')
def plot(graph, period):
    graph = graph.replace('-', '_')
    return render_template('plot.html', graph=graph, period=period)

@app.route('/get/<label>/interval/<int:interval>')
@app.route('/get/<label>/start/<start>')
@app.route('/get/<label>/start/<start>/end/<end>')
@app.route('/get/<label>/end/<end>')
@app.route('/get/<label>/count/<int:count>')
def get(label, interval=None, start=None, end=None, count=None):
    data = {'label': label}
    conn = pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['passwd'],
        db='idb', charset='utf8')
    cur = conn.cursor()
    sql = 'SELECT data.value, data.updated FROM data WHERE data.label="{}" '.format(label)
    if interval is not None:
        sql = 'SELECT data.value, data.updated FROM data \
            WHERE data.label="{}" \
            AND NOW(6)-INTERVAL {} SECOND < data.updated \
            ORDER BY data.updated ASC'.format(label, interval)
    elif start is not None:
        if end is not None:
            sql = 'SELECT data.value, data.updated FROM data WHERE data.label="{}" \
                AND {}<data.updated<{} \
                ORDER BY data.updated ASC'.format(label, start, end)
        else:
            sql = 'SELECT data.value, data.updated FROM data WHERE data.label="{}" \
                AND {}<data.updated \
                ORDER BY data.updated ASC'.format(label, start)
    elif end is not None:
        sql = 'SELECT data.value, data.updated FROM data WHERE data.label="{}" \
            AND data.updated<{} \
            ORDER BY data.updated ASC'.format(label, end)
    elif count is not None:
        sql = 'SELECT * FROM ( \
            SELECT data.value, data.updated FROM data WHERE data.label="{}" \
            ORDER BY data.updated DESC LIMIT {} \
        ) AS alias \
        ORDER BY alias.updated ASC'.format(label, count)
    cur.execute(sql)
    rows = cur.fetchall()
    data['data'] = []
    for r in rows:
        data['data'].append({'val': r[0], 'updated': str(r[1])})
    cur.close()
    conn.close()
    return json.dumps(data)

@app.route('/static/<path:path>')
def loadStatic(path):
    return url_for('static', path=path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
