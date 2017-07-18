from flask import Flask, url_for, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('monitor'))

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@app.route('/static/<path:path>')
def loadStatic(path):
    return url_for('static', path=path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
