#these are the imports
from flask import Flask, render_template, request
import json

import main

app = Flask(__name__)

#this is the decorator. it shows what to return when i go to the website
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/gradeDisplay', methods=['POST'])
def authenticate():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    print(username+" "+password)


    #replace real grade getter with stored grades to speed up time

    returnStoredGrades=False
    if returnStoredGrades:
        return render_template("gradeDisplay.html", grades=main.getStoredGrades())
    else:
        return render_template("gradeDisplay.html", grades=main.gradeGetter.getGrades(username,password))


if __name__ == "__main__":
    app.run(debug=True)
