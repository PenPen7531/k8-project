from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient
import hashlib
import requests
import datetime
import json

app = Flask(__name__)

client = MongoClient('mongodb://mongodb:27017/')

db = client.db1

app.secret_key="session_key666"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=="GET":
        session['user']=None
        return render_template("home.html", error=False)

    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        encoded = hashlib.sha256(password.encode('ASCII')).hexdigest()
        print(encoded)
        if username.upper() == 'ADMIN':
            reponse = requests.get(f"http://auth-service:3000/api/users/{username.upper()}")
            data = json.loads(reponse.content)
            
            if encoded == data['user_hash']:
                session['user']='yes'
                return redirect("/data")

    return render_template('home.html', error=True)
   


@app.route("/data", methods=['GET', 'POST'])
def entry():
    
    if session['user'] == 'yes':
        if request.method == "GET":
            grades = db.students.find()[0]
            count = grades['grade_count']
            mean = grades['grade_mean']
            min = grades['grade_min']
            max = grades['grade_max']

            return render_template('index.html', count=count, mean=mean, min=min, max=max)          

    return render_template('invalid.html')


if __name__ == "__main__":
    app.run()