from flask import Flask , render_template , url_for
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import logging as log
import boto3


import Login


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)
app.secret_key = 'THISISASECRETKEY'
app.config['SESSION_TYPE'] = 'filesystem'




# @app.route("/home", methods=["GET", "POST"])
# def login():
#     log.warning('<---------Inside Login------------->')
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

        
#         flg,error = Login.login(username,password)
#         if flg:
#             # Authentication successful, set session variable
#             session["username"] = username
#             return redirect(url_for("dashboard"))
#         else:
#             # Authentication failed, show error message
#             return render_template("home.html", error=error)

#     return render_template("home.html")



# @app.route("/logout")
# def logout():
#     log.warning('<---------Inside LogOut------------->')
#     # Clear the session and log the user out
#     session.pop("username", None)
#     return redirect(url_for("login"))



# @app.route("/dashboard")
# def dashboard():
#     log.warning('<---------Inside DashBoard------------->')
#     # Check if user is logged in (session exists)
#     if "username" in session:
#         return f"<h1>Welcome, {session['username']}!</h1>"
#     else:
#         return redirect(url_for("login"))




@app.route("/home", methods=["GET", "POST"])
def login():
    log.warning('<---------Inside Login------------->')
    if request.method == "POST":
        role = request.form["role"]

        if role == 'role1':
            print('role1')
            redirect_url = redirectRole1()

            return redirect(redirect_url,code=302)
            
            # login()
        elif role == 'role2':
            print('role2')
            # login()
    return render_template("home.html")




def redirectRole1():
    COGNITO_HOSTED_UI = "https://myap.auth.eu-west-1.amazoncognito.com"
    APP_CLIENT_ID = "2onui627bl53k8gcooc99f984o"
    REDIRECT_URI = "http://localhost:5000/home"  # Where Cognito will redirect after authentication
    RESPONSE_TYPE = "code"  # Use "code" for Authorization code grant, or "token" for Implicit grant
    SCOPE = "email+openid+phone"  # OpenID scope, can be adjusted based on needs
    cognito_auth_url = f"{COGNITO_HOSTED_UI}/login?response_type={RESPONSE_TYPE}&client_id={APP_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return cognito_auth_url


if __name__ == "__main__":
    app.run(debug=False)
    