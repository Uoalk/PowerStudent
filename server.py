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
    email = request.form['email']
    emailPassword = request.form['emailPassword']
    print(username+" "+password+ email)

    #replace real grade getter with stored grades to speed up time
    ####does this help idk --> https://beenje.github.io/blog/posts/running-background-tasks-with-flask-and-rq/
    while(True):
        changes = main.getChanges(main.getStoredGrades(), main.gradeGetter.getGrades(username,password))
        gradeData = main.gradeGetter.getGrades(username,password)
        if main.getChanges(main.getStoredGrades(), main.gradeGetter.getGrades(username,password)) != "":
            return render_template("gradeDisplay.html", grades=main.getStoredGrades())
        else:
            main.emailer.send_email(email,emailPassword,email,"Powerschool update", changes)
            with open('gradeData.json', 'w') as file:
                json.dump(gradeData, file, indent=2)
            return render_template("gradeDisplay.html", grades=main.gradeGetter.getGrades(username,password))


if __name__ == "__main__":
    app.run(debug=True)
