from crypt import methods
from flask import Flask
from flask import render_template,request,redirect
import API
import pandas as pd
# create the app
app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    with app.app_context():
        if request.method =='GET':
            return  render_template('index.html')
        if request.method == 'POST':
            text_en = request.form.get('en')
            text_jp = request.form.get('jp')
            df = API.createPage(text_en,text_jp)
            header = df.columns
            record = df.values.tolist()
            return render_template('index.html' , text_en = text_en, text_jp=text_jp,header=header, record=record )







