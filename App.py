from flask import Flask , render_template , url_for
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session,Response
import logging as log
import boto3
import SignUp
import json
import Login
import requests
import os
import base64


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
            username = request.form.get('loginId')
            pwd = request.form.get('pwd')

            resp,ses = SignUp.SignIn(username,pwd)

            if resp == 'Error':
                return render_template("home.html",msg=resp,username=username)
            
            elif resp == 'No MFA':
                return render_template("home.html",msg='logged in',username=username)
            
            elif resp == 'MFA':
                session = ses
                return render_template("OTP-SignIn.html",msg='MFA',username=username,)
        

            return render_template("home.html")

        elif flg =='signup':
            print('Go to signup')
            return render_template("signup.html")

        elif flg =='3FA':
            log.warning('<---------Inside 3FA------------->')
            redirect_url = redirectRole2()

            image_data = request.form['image']
            image_data = base64.b64decode(image_data)
            image_path = os.path.join('images', 'captured_image.png')

            try:
                with open(image_path, 'wb') as f:
                    f.write(image_data)
            except Exception as e:
                log.warning('Error--------------->'+str(e))

            return redirect(redirect_url,code=302)
        
    return render_template("home.html")




def redirectRole1():
    COGNITO_HOSTED_UI = "https://myap.auth.eu-west-1.amazoncognito.com"
    APP_CLIENT_ID = "2onui627bl53k8gcooc99f984o"
    REDIRECT_URI = "http://localhost:5000/awsRedirect"  # Where Cognito will redirect after authentication
    RESPONSE_TYPE = "code"  # Use "code" for Authorization code grant, or "token" for Implicit grant
    SCOPE = "email+openid+phone"  # OpenID scope, can be adjusted based on needs
    cognito_auth_url = f"{COGNITO_HOSTED_UI}/login?response_type={RESPONSE_TYPE}&client_id={APP_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return cognito_auth_url

def redirectRole2():
    COGNITO_HOSTED_UI = "https://srushti-application.auth.eu-west-1.amazoncognito.com"
    APP_CLIENT_ID = "19k9ue27jvgsvbrfts5odnlrf6"
    REDIRECT_URI = "http://localhost:5000/signIn3"  # Where Cognito will redirect after authentication
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
            pwd = request.form.get('password')
            phone = request.form.get('phone')
        
            signUpFlg = SignUp.SignUpSDK(username,pwd,phone)
            if signUpFlg:
                msg = "Signup successful! Please check your phone for MFA code."
                
                #return render_template("OTP.html",otpFlg=True,msg = msg,username=username)
                return render_template('verify_totp', username=username)
            
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
def submitOtpSignUp():
    log.warning('<---------Inside Submit-Otp SignUP------------->')
    if request.method == "POST":
            username = request.form.get('username')
            mfa_code = request.form.get('otp')
            try:
                signUpFlg = SignUp.confirmation(username,mfa_code)

                if signUpFlg:

                    msg = "Signup successful! "
                    return render_template("signup.html",otpFlg=False,msg = msg)
                
                else:
                    msg = "Error in Creation of Account."
                    return render_template("signup.html",otpFlg=False,msg = msg)
            except Exception as e:
                log.warning('<----Error--------------->'+str(e))
                return render_template("signup.html",otpFlg=False)


@app.route("/submitotp", methods=["GET", "POST"])
def submitOtp():
    log.warning('<---------Inside OTP------------->')
    if request.method == "POST":
        username = request.form.get('email')
        mfa_code = request.form.get('otp')
        ses = request['session']


        try:
            flg,resp = SignUp.signin_mfa(username,mfa_code,ses)

        except Exception as e:
            log.warning('<----------------Exception Occured---------------->'+e)


        return render_template("home.html",msg='logged in',username=username)
    else:
        return render_template("OTP.html")


@app.route('/awsRedirect',methods=['GET'])
def awsRedirect():
    log.warning('<---------Inside awsRedirect------------->')

    if request.method == "GET":


        arn = 'arn:aws:iam::474672952960:role/ForDev'

        
        try:
            redirectUrl = SignUp.AwsRedirect(arn)
        except Exception as e:
            log.warning('<----------Exception Occured---------->')
            log.warning('Error---------------->'+str(e))
            redirectUrl = 'home.html'
        return redirect(redirectUrl)

        
@app.route('/verify_totp/<username>', methods=['GET', 'POST'])
def verify_totp(username):
    log.warning('<---------Inside verify_totp------------->')
    if request.method == 'POST':
        totp_code = request.form['totp_code']


        try:

            verify = SignUp.verify_totp(username,totp_code)


            if verify:
                return render_template("home.html")
            else:
                return render_template("signup.html")




        except Exception as e:
            log.warning('Error----------->'+str(e))
            return render_template("signup.html")

        
        # # Fetch the TOTP secret from Cognito
        # user = client.admin_get_user(
        #     UserPoolId=USER_POOL_ID,
        #     Username=username
        # )
        # totp_secret = [attr['Value'] for attr in user['UserAttributes'] if attr['Name'] == 'custom:totp_secret'][0]
        
        # totp = pyotp.TOTP(totp_secret)
        # if totp.verify(totp_code):
        #     return "TOTP verified successfully!"
        # else:
        #     return "Invalid TOTP code. Please try again."

    return render_template('verify_totp.html', username=username, qr_path=f"{username}_qr.png")

@app.route('/signIn3', methods=['GET'])
def signIn3():
    log.warning('<------------Inside SignIn3------------>')
    if request.method == "POST":
        username = session['username']
        render_template("signIn3FA.html")


    elif request.method == "GET":
        #username = session['username']
        code = request.args.get('code')
        tokens = get_tokens(code)

        if tokens:
            user_info = get_user_info(tokens['access_token'])
            username = user_info['username']
            print(username)

            #For SignUp
            try:
                signUpFlg = SignUp.CheckFile(username)
            except Exception as e:
                log.warning('Error-------------->'+str(e))
                return render_template('home.html')

            if signUpFlg:
                log.warning('For Sign IN')
                try:
                    # with open('images\captured_image.png', 'rb') as file:
                    #     image_data = file.read()

                    image_data='images\captured_image.png'
                    matches,code = SignUp.compare(image_data,username)

                    if code == 200:
                        if int(matches) > 70:
                            session["username"] = username
                            removeFile()
                            arn = 'arn:aws:iam::474672952960:role/For_Sec'
                            redirectUrl = SignUp.AwsRedirect(arn)
                            return render_template('Dashboard.html',msg='Success')
                        else:
                            removeFile()
                            return render_template('Dashboard.html',msg='Match failed')
                        
                except Exception as e:
                    log.warning('Error----------->'+str(e))
                    removeFile()
                    return render_template('home.html')

                            
            else:

                print('For SignUP')
                try:
                    # with open('images\captured_image.png', 'rb') as file:
                    #     image_data = file
                    image_data = 'images\captured_image.png'
                    ref,code = SignUp.upload(image_data,username)
                    

                    if code == 200:
                        session["username"] = username
                        removeFile()
                        arn = 'arn:aws:iam::474672952960:role/sec'
                        redirectUrl = SignUp.AwsRedirect(arn)

                        return render_template('Dashboard.html',msg='Success')


                except Exception as e:
                    log.warning('Error--------------->'+str(e))


            render_template("signIn3FA.html")
            # Now you have the username and can use it in your application
            # ...
        else:
            return "Error during authentication", 400



        render_template("signIn3FA.html")


def get_user_info(access_token):
    user_info_url = "https://srushti-application.auth.eu-west-1.amazoncognito.com/oauth2/userInfo"
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(user_info_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

def get_tokens(code):
    token_url = "https://srushti-application.auth.eu-west-1.amazoncognito.com/oauth2/token"
    clientId = "19k9ue27jvgsvbrfts5odnlrf6"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': '19k9ue27jvgsvbrfts5odnlrf6',
        'code': code,
        'redirect_uri': 'http://localhost:5000/signIn3'
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
    except Exception as e:
        log.warning('Error----------------->'+str(e))
    
    if response.status_code == 200:
        return response.json()
    return None




def removeFile():
    file_path = 'images/captured_image.png'

    # Check if the file exists and then delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted!")
    else:
        print(f"The file {file_path} does not exist.")
if __name__ == "__main__":
    app.run(debug=False)
    