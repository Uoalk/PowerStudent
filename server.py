#these are the imports
from flask import Flask, render_template, request
import json

import main

app = Flask(__name__)

#this is the decorator. it shows what to return when i go to the website
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/authenticate', methods=['POST'])
def authenticate():
    print(request.form)
    username = request.form['username']
    password = request.form['password']
    print(username+" "+password)
    return json.dumps(main.gradeGetter.getGrades(username,password))

if __name__ == "__main__":
    app.run(debug=True)
