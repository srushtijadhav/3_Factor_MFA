from flask import Flask, render_template, request, redirect, url_for, session
import DAO

def login(username,password):
    flg = False
    error = None

    USERNAME,PASSWORD,role = DAO.login_credentials(username)
    if username == USERNAME and password == PASSWORD:
        # Authentication successful, set session variable
        flg=True
        return  flg,error
    else:
        # Authentication failed, show error message
        error="Invalid credentials"
        return  flg,error

    return flg,error