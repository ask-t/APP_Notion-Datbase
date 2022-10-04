from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def hello_world():
    return  render_template('index.html')

@app.route("/practice")
def hello_practice():
    return render_template('sample.html')