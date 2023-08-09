from flask import Flask

app2 = Flask(__name__)


@app2.route('/img')
def imgCapture():
    return None
