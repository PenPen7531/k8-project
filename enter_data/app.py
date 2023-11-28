from flask import Flask, render_template, redirect, request, session, jsonify
import datetime
import requests
import hashlib
import json
import connexion
from connexion import NoContent
from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector
import yaml
import time

count = 0
while count < 10:
    try:
        db_conn = mysql.connector.connect(host="mysql-db", user="root", password="P@ssw0rd", database="users")
        db_cursor = db_conn.cursor(buffered=True)
        break
    except:
        print("Retrying in 10 seconds")
        time.sleep(10)

app = Flask(__name__)

app.secret_key="session_key666"


@app.route("/", methods=['GET', 'POST'])
def home():
    # try:
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
                return redirect("/submit")
            
        


    return render_template('home.html', error=True)
   


@app.route("/submit", methods=['GET', 'POST'])
def entry():
    
    if session['user'] == 'yes':
        if request.method == "GET":
            return render_template('submit.html')
        
        if request.method == "POST":
            data = request.form.get('grade')
            body = {
                "grade": int(data)
            }
            db_cursor = db_conn.cursor(buffered=True)
            time_now = datetime.datetime.now()
        
  
            
        
            
            db_cursor.execute(f"Insert into users.data(grade, date_created) VALUES ({data}, '{time_now}')")
            db_conn.commit()
        

            return render_template("submit.html", completed=True)
        
            

    return render_template('invalid.html')
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)