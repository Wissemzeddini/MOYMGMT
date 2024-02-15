from flask import Flask, url_for,  redirect, render_template, request,session, send_from_directory
import os
from Models.user import User
import hashlib
import time
import json

app = Flask(__name__)
app.secret_key = 'moymgmt(:Gh/.>.*/{)]'
# Set the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def check_session():
    if 'username' in session:
        return True
    return False

def loadJsonFile(filename="categories.json"):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

#generate a unique name based on hashed timestamp
def generate_unique_filename(filename):
    _, file_extension = os.path.splitext(filename)
    timestamp = str(time.time())
    hash_object = hashlib.md5(timestamp.encode() + filename.encode())
    return hash_object.hexdigest() + file_extension

@app.route("/")
def index():
    if check_session():
        print(session['username'])
        return render_template("index.html",session=session,jsonObj=loadJsonFile())
    return redirect('/login')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/authentification", methods=['GET', 'POST'])
def auth():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
    except Exception as e:
        return str(e)
    user = User(username,"email@example.com","logo.png",password)
    if user.authenticate():
        id,username,email,picture = user.getUser()
        session["username"] = username
        session["userId"] = id
        session["email"] = email
        session["picture"] = picture
        return redirect('/')
    return render_template("login.html",error="Username or Password incorrect.")

@app.route("/register")
def register():
    return render_template("register.html",error=None)

@app.route("/user/new", methods=['GET', 'POST'])
def addUser():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        file = request.files['file']
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if( not password == confirm):
            return render_template("register.html",error="The confirm password is different.")
    except Exception as e:
        return render_template("register.html",error=str(e))
    if file:
        unique_filename = generate_unique_filename(file.filename)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filename)
        print('File uploaded successfully.')
    user = User(username,email,unique_filename,password)
    if user.register():
        return redirect('/login')
    return render_template("register.html",error="User already existe!")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('userId', None)
    session.pop('email', None)
    session.pop('picture', None)
    return redirect('login')
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/saveItem', methods=['GET', 'POST'])
def save_expense():
    category =  request.form.get('subcategory')
    name = request.form.get('items_name')
    price = request.form.get('items_price')
    quantity = request.form.get('items_quantity')
    region = request.form.get('items_region')


if __name__=="__main__":
    app.run(debug=True)