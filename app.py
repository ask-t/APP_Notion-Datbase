from crypt import methods
from flask import Flask
from flask import render_template,request,redirect
import pytz
# create the app
app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    if request.method =='GET':
        with app.app_context():
            posts = Post.query.all()
    return  render_template('index.html',posts=posts)

@app.route("/practice")
def hello_practice():
    return render_template('sample.html')





