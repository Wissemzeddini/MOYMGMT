from flask import Flask, url_for,  redirect, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__=="__main__":
    app.run(debug=True)