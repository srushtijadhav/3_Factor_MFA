from flask import Flask , render_template , url_for
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session,Response
import logging as log
import boto3
import SignUp
import json


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


        flg = request.form["flag"]

        if flg == '2FA':
             log.warning('<---------Inside 2FA------------->')
             redirect_url = redirectRole1()

             return redirect(redirect_url,code=302)
        
        elif flg == 'login':
            print ('Login SDK code')
            log.warning('<---------Inside 3FA------------->')
            username = request.form.get('email')
            mfa_code = request.form.get('password')

            resp,ses = SignUp.SignIn()

            if resp == 'Error':
                return render_template("home.html",msg=resp,username=username)
            
            elif resp == 'No MFA':
                return render_template("home.html",msg='logged in',username=username)
            
            elif resp == 'MFA':
                session = ses
                return render_template("OTP.html",msg='MFA',username=username,)
        

            return render_template("home.html")

        elif flg =='signup':
            print('Go to signup')
            return render_template("signup.html")

        # role = request.form["role"]
        # if role == 'role1':
        #     print('role1')
        #     redirect_url = redirectRole1()

        #     return redirect(redirect_url,code=302)
            
        #     # login()
        # elif role == 'role2':
        #     print('role2')
        #     # login()
    return render_template("home.html")




def redirectRole1():
    COGNITO_HOSTED_UI = "https://myap.auth.eu-west-1.amazoncognito.com"
    APP_CLIENT_ID = "2onui627bl53k8gcooc99f984o"
    REDIRECT_URI = "http://localhost:5000/home"  # Where Cognito will redirect after authentication
    RESPONSE_TYPE = "code"  # Use "code" for Authorization code grant, or "token" for Implicit grant
    SCOPE = "email+openid+phone"  # OpenID scope, can be adjusted based on needs
    cognito_auth_url = f"{COGNITO_HOSTED_UI}/login?response_type={RESPONSE_TYPE}&client_id={APP_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return cognito_auth_url




@app.route("/signup", methods=["GET", "POST"])
def signupPg():
    log.warning('<---------Inside Login------------->')
    if request.method == "POST":

        flg = request.form["flag"]

        if flg == 'signup':

            username = request.form.get('email')
            mfa_code = request.form.get('password')
            phone = request.form.get('phone')
        
            signUpFlg = SignUp.SignUpSDK(username,mfa_code,phone)
            if signUpFlg:
                msg = "Signup successful! Please check your phone for MFA code."
                
                return render_template("signup.html",otpFlg=True,msg = msg)
            
            else:
                msg = "Error in Creation of Account."
                return render_template("signup.html",otpFlg=False,msg = msg)
            

        elif flg == '2FA':
            username = request.form.get('username')
            mfa_code = request.form.get('OTP')

            signUpFlg = SignUp.confirmation(username,mfa_code)

            if signUpFlg:

                msg = "Signup successful! "
                return render_template("signup.html",otpFlg=False,msg = msg)
            
            else:
                msg = "Error in Creation of Account."
                return render_template("signup.html",otpFlg=False,msg = msg)
    


    return render_template("signup.html")



@app.route("/submit-otp", methods=["GET", "POST"])
def submitOtp():
    log.warning('<---------Inside Login------------->')
    if request.method == "POST":
        username = request.form.get('email')
        mfa_code = request.form.get('otp')
        ses = request['session']


        try:
            flg,resp = SignUp.signin_mfa(username,mfa_code,ses)

        except Exception as e:
            log.warning('<----------------Exception Occured---------------->'+e)


        return render_template("home.html",msg='logged in',username=username)


if __name__ == "__main__":
    app.run(debug=False)
    