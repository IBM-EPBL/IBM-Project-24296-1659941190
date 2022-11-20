from flask import Flask, redirect, url_for, request, render_template, session
import ibm_db
from flask_session import Session

conn = None

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def connect():
    global conn 
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dxy32089;PWD=75PDKFFPQjkfYtNz",'','')


@app.route('/')
def base():
    return render_template('index.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if(conn == None):
            connect()
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phno = request.form.get('phno')
        name = request.form.get('name')
        stmt = ibm_db.exec_immediate(conn, "insert into login(username,password,name,phonenumber,email) values ('"+username+"', '"+password+"', '"+name+"', "+phno+", '"+email+"');")
        if(ibm_db.num_rows(stmt)>0):
            return redirect("/")
    return render_template("signup.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if(conn == None):
            connect()
        stmt = ibm_db.exec_immediate(conn, "Select * from login where email = '"+username+"' and password = '"+password+"' ")
        result = ibm_db.fetch_assoc(stmt)
        if(result):
            session["username"] = result["USERNAME"]
            session["password"] = result["PASSWORD"]
            session["email"] = result["EMAIL"]
            session["phonenumber"] = result["PHONENUMBER"]
            return render_template('home.html')
        else:
            return "wrong credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    conn = None
    session["username"] = None
    session["password"] = None
    session["email"] = None
    session["phonenumber"] = None
    return redirect("/")

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000)