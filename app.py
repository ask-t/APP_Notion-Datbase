from crypt import methods
from flask import Flask
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
# create the app
app = Flask(__name__)

# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default = datetime.now(pytz.timezone('US/Hawaii')) )

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
    if request.method =='POST':
        with app.app_context():
            title = request.form.get('title')
            body = request.form.get('body')
            post=Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        return redirect('/')
    else:
        return  render_template('create.html')