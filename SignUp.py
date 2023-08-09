
import boto3
from flask import Flask, request, render_template_string
import logging as log

# Initialize the boto3 client for Cognito
# client = boto3.client('cognito-idp', region_name='eu-west-1')

# USER_POOL_ID = 'eu-west-1_zKGLIBXYH'
# CLIENT_ID = '48nhuo85q76h6l3to96rf8f80m'



def SignUpSDK(username,password,phone_number):
    log.warning('<----------------Inside SignUp SignUpSDK----------------->')

    client = boto3.client('cognito-idp', region_name='eu-west-1')
    USER_POOL_ID = 'eu-west-1_zKGLIBXYH'
    CLIENT_ID = '48nhuo85q76h6l3to96rf8f80m'
    try:
            response = client.sign_up(
                ClientId=CLIENT_ID,
                Username=username,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'phone_number',
                        'Value': phone_number
                    },
                ]
            )
            log.warning("Signup successful! Please check your phone for MFA code.")
            return True
    #"Signup successful! Please check your phone for MFA code."
    except Exception as e:
            log.warning("<------------Failed to signup: ------->"+str(e))
            return False
 
    return None


def confirmation(username ,mfa_code ):
    log.warning('<----------------Inside SignUp confirmation----------------->')

    client = boto3.client('cognito-idp', region_name='eu-west-1')
    USER_POOL_ID = 'eu-west-1_zKGLIBXYH'
    CLIENT_ID = '48nhuo85q76h6l3to96rf8f80m'
    try:
        response = client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=mfa_code
        )

        log.WARNING("<---------Signup confirmed!---------->")
        return  True
    except Exception as e:

        log.WARNING("<----------Failed to confirm signup:-------->"+e)
        return False
    
    return None




