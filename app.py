from crypt import methods
from flask import Flask
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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

@app.route("/create",methods=['GET','POST'])
def create():
    with app.app_context():
        if request.method =='POST':
            title = request.form.get('title')
            body = request.form.get('body')
            post=Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        else:
            return  render_template('create.html')




