from flask import Flask , render_template , url_for
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import logging as log


import Login


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)
app.secret_key = 'THISISASECRETKEY'
app.config['SESSION_TYPE'] = 'filesystem'



@app.route("/", methods=["GET", "POST"])
def login():
    log.warning('<---------Inside Login------------->')
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        
        flg,error = Login.login(username,password)
        if flg:
            # Authentication successful, set session variable
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            # Authentication failed, show error message
            return render_template("login.html", error=error)

    return render_template("login.html")



@app.route("/logout")
def logout():
    log.warning('<---------Inside LogOut------------->')
    # Clear the session and log the user out
    session.pop("username", None)
    return redirect(url_for("login"))



@app.route("/dashboard")
def dashboard():
    log.warning('<---------Inside DashBoard------------->')
    # Check if user is logged in (session exists)
    if "username" in session:
        return f"<h1>Welcome, {session['username']}!</h1>"
    else:
        return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)