#these are the imports
from flask import Flask, render_template


app = Flask(__name__)

#this is the decorator. it shows what to return when i go to the website
@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
