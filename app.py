from flask import Flask, url_for,  redirect, render_template, request,session
from Models.user import User

app = Flask(__name__)
app.secret_key = 'moymgmt(:Gh/.>.*/{)]'

def check_session():
    if 'username' in session:
        return True
    return False

@app.route("/")
def index():
    if check_session():
        print(session['username'])
        return render_template("index.html")
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
    return redirect('/login')

@app.route("/register")
def register():
    return render_template("register.html",error=None)

@app.route("/user/new", methods=['GET', 'POST'])
def addUser():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        file = request.form.get('file')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if( not password == confirm):
            return render_template("register.html",error="The confirm password is different.")
    except Exception as e:
        return render_template("register.html",error=str(e))
    user = User(username,email,file,password)
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
    

if __name__=="__main__":
    app.run(debug=True)