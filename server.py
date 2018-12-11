#This runs the webserver that allows users to sign up and see thir grades

#these are the imports
from flask import Flask, render_template, request
import json
import gradeAlerter, gradeGetter
import main
import uuid
import encryption

masterPw="12345"
app = Flask(__name__)


#generates a random string of characters
def genSalt():
    return str(uuid.uuid4().hex)


#adds a user based on submitted data
def addUser(usr,pw,email,frequency):
    userData=json.loads(open("names.JSON").read())
    salt=genSalt()
    encryptedPW=encryption.encrypt(pw,masterPw,salt)

    data={
        "email":email,
        "username":usr,
        "salt":salt,
        "password":str(encryptedPW),
        "frequency":frequency,
        "cachedGrades":{},
    }
    userData[usr]=data

    #save changes to json
    with open('names.json', 'w') as outfile:
        json.dump(userData, outfile, sort_keys = True, indent = 4,
               ensure_ascii = False)



#this is the decorator. it shows what to return when i go to the website
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


#path to submit grade data
@app.route('/submitDetails', methods=["post"])
def submitDetails():

    username = request.form['username']
    password = request.form['password']
    #make sure that the username and password are valid
    if(not gradeGetter.verifyUsernamePassword(username,password)):
        return "We were unable to verify your username and password. You have not been added to the database."

    addUser(username,password,request.form['email'],request.form['frequency'])



    return render_template("success.html")

#renders a page to display a users grades
@app.route('/gradeDisplay', methods=['POST'])
def authenticate():

    userData=json.loads(open("names.JSON").read())[request.form["username"]]

    return render_template("gradeDisplay.html", grades=userData["cachedGrades"])



    #replace real grade getter with stored grades to speed up time
    ####does this help idk --> https://beenje.github.io/blog/posts/running-background-tasks-with-flask-and-rq/
    #um this is wrong but i think this youtube video could help https://www.youtube.com/watch?v=Kcka5WBMktw



if __name__ == "__main__":
    app.run(debug=True)
