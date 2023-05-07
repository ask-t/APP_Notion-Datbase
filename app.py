from flask import Flask
from flask import render_template,request,send_file
import API
import pandas as pd
# create the app
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    with app.app_context():
        if request.method == "GET":
            return render_template("index.html")
        elif request.method == "POST":
            if request.form["button"]  == "read database":
                databaseId = request.form.get("data")
                try:
                    column = API.fetchData(databaseId)
                    return render_template("index2.html", column = column, databaseId = databaseId)
                except:
                    message = "We couldn't find the database. Try again."
                    return render_template("index.html", message = message)
            elif request.form["button"]  == "create new":
                databaseId = request.form.get("data")
                column = API.fetchData(databaseId)
                row = []
                for i in column:
                    b = request.form.get(i[0])
                    i.append(b)
                    row.append(i)
                df = API.createPage(row,databaseId)
                header = df.columns
                record = df.values.tolist()
                return render_template('index2.html',header=header, record=record,column = column,databaseId=databaseId)
            elif request.form["button"] == "CSV":
                databaseId = request.form.get("data")
                API.create_csv(databaseId)
                text_en = "Succeed to create CSV"
                downloadFile = "to_csv_out.csv"
                return send_file(downloadFile,as_attachment = True)






