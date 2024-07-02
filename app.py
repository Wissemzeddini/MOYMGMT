from flask import Flask, url_for,  redirect, render_template, request,session, send_from_directory
import os
from Models.user import User
from Models.dbmanager import fetchDataWithoutParams
from Models.item import Item,Ticket
import hashlib
import time
import json
from datetime import datetime
from math import ceil

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

def get_regions():
    rows = fetchDataWithoutParams("select * from regions;")
    return rows
#generate a unique name based on hashed timestamp
def generate_unique_filename(filename):
    _, file_extension = os.path.splitext(filename)
    timestamp = str(time.time())
    hash_object = hashlib.md5(timestamp.encode() + filename.encode())
    return hash_object.hexdigest() + file_extension

def getDefaultCurrency():
    rows = fetchDataWithoutParams("select * from currencies limit 1;")
    return rows[0][0]

def get_stats():
    daily = fetchDataWithoutParams("SELECT COALESCE(SUM(current_price), 0) as daily FROM items WHERE SUBSTR(createdAt, 1, 10) = DATE('now');")
    weekly = fetchDataWithoutParams("SELECT COALESCE(SUM(current_price), 0) as weekly_expense FROM items WHERE strftime('%Y-%m-%W', createdAt) = strftime('%Y-%m-%W', 'now', 'localtime');")
    monthly = fetchDataWithoutParams("SELECT COALESCE(SUM(current_price), 0) as monthly_expense FROM items WHERE strftime('%Y-%m', createdAt) = strftime('%Y-%m', 'now', 'localtime');")
    total = fetchDataWithoutParams("SELECT COALESCE(SUM(current_price), 0) as total FROM items;")
    return [daily[0][0], weekly[0][0], monthly[0][0], total[0][0]]

@app.route("/")
def index():
    if check_session():
        print(session['username'])
        return render_template("index.html",session=session,jsonObj=loadJsonFile(),regions=get_regions(), stats=get_stats())
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
    category = request.form.get('category')
    subcategory =  request.form.get('subcategory')
    name = request.form.get('itemName')
    price = request.form.get('itemPrice')
    quantity = request.form.get('itemQuantity')
    region = request.form.get('itemRegion')
    currency = getDefaultCurrency()
    print(category,subcategory,name,price,quantity,region,currency,session.get("userId"))
    itm = Item(category,subcategory,name,price,quantity,region,currency,session.get("userId"))
    itm.saveItem()
    return redirect('/')

@app.route('/tickets')
def tickets():
    user_id = session.get("userId")
    if not user_id:
        return redirect(url_for('login'))  # Redirect to login if user is not authenticated

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    offset = (page - 1) * per_page

    tk = Ticket(user_id)
    total_tickets = len(tk.getAllTicketsCount())  # You may need a separate method to count the total tickets
    tickets = tk.getAllTickets(offset, per_page)
    total_pages = ceil(total_tickets / per_page)

    return render_template(
        "tickets.html",
        session=session,
        jsonObj=loadJsonFile(),
        tickets=tickets,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

if __name__=="__main__":
    app.run(debug=True)