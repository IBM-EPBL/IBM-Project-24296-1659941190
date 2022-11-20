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
    conn = ibm_db.connect("AUTHENTICATION=SERVER;DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tmj80232;PWD=XFJsY2e4yqV8KpXS",'','')


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