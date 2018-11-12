#these are the imports
from flask import Flask, render_template, request
import json
import gradeAlerter, gradeGetter
import main
import uuid

masterPw=1235
app = Flask(__name__)


def genSalt():
    return str(uuid.uuid4().hex)

def xor_crypt_string(plaintext, key):#
    ciphertext = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(plaintext, cycle(key)))
    return ciphertext.encode('base64')

def xor_decrypt_string(ciphertext, key):
    ciphertext = ciphertext.decode('base64')
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(ciphertext, cycle(key)))

def addUser(usr,pw,email,frequency):
    userData=json.loads(open("names.JSON").read())
    salt=genSalt()

    userData[usr]=""



#this is the decorator. it shows what to return when i go to the website
@app.route('/')
def index():
    return render_template("bootstrap/index.html")


@app.route('/signup')
def signup():
    return render_template("bootstrap/signup.html")

@app.route('/submitDetails', methods=["post"])
def submitDetails():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    if(not gradeGetter.verifyUsernamePassword(username,password)):
        return "We were unable to verify your username and password. You have not been added to the database."

    addUser(username,password,request.form['email'],request.form['frequency'])



    return "You have been added the database"

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
    addUser("gfitez20","","grantfitez@gmail.com","ASAP")
    app.run(debug=True)
