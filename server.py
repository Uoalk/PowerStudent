#these are the imports
from flask import Flask, render_template, request
import json
import gradeAlerter
import main

app = Flask(__name__)
data = {}

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

    
    data[username] = {"username":username, "password":password, "email":email, "email_password":emailPassword}
    with open("names.JSON", 'w') as file:
        json.dump(data, file, indent=2)
        return render_template("gradeDisplay.html", grades=main.getStoredGrades())



    #replace real grade getter with stored grades to speed up time
    ####does this help idk --> https://beenje.github.io/blog/posts/running-background-tasks-with-flask-and-rq/
    #um this is wrong but i think this youtube video could help https://www.youtube.com/watch?v=Kcka5WBMktw



if __name__ == "__main__":
    app.run(debug=True)
