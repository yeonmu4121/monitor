from flask import Flask, url_for, render_template, redirect
import json

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

@app.route('/plot/<graph>/interval/<int:interval>')
def plot(graph, interval):
    graph = graph.replace('-', '_')
    return render_template('plot.html', graph=graph, interval=interval)

@app.route('/static/<path:path>')
def loadStatic(path):
    return url_for('static', path=path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
