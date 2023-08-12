
import boto3
from flask import Flask, request, render_template_string,jsonify
import logging as log
import uuid
import json
import requests

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


def SignIn(username,pwd):
     log.warning('<----------------Inside SignIn confirmation----------------->')
     client = boto3.client('cognito-idp', region_name='eu-west-1')
     USER_POOL_ID = 'eu-west-1_zKGLIBXYH'
     CLIENT_ID = '48nhuo85q76h6l3to96rf8f80m'
     try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': pwd
            }
        )

        if response.get('ChallengeName') == 'SMS_MFA':
            log.warning('<----------------Inside SignIn MFA requested----------------->')
            return 'MFA', response['session']

        return 'No MFA', response['session']

     except Exception as e:
        log.warning('<----------Exception occured------->'+e)
        return 'Error', response['session']



def signin_mfa(username,otp,ses):
    log.warning('<----------------Inside SignIn confirmation----------------->')
    client = boto3.client('cognito-idp', region_name='eu-west-1')
    USER_POOL_ID = 'eu-west-1_zKGLIBXYH'
    CLIENT_ID = '48nhuo85q76h6l3to96rf8f80m'

    try:
        response = client.respond_to_auth_challenge(
            ClientId=CLIENT_ID,
            ChallengeName='SMS_MFA',
            Session=ses,
            ChallengeResponses={
                'USERNAME': username,
                'SMS_MFA_CODE': otp
            }
        )

        log.warning('<----------------Signed In----------------->')

        return True, response

    except Exception as e:
        log.warning('<----------------Exception Occured---------------->'+e)
        return False, response
    




#
#    AccessKey




def upload(file,uniqueName):
    log.warning('<----------------Inside SignUp upload----------------->')
    # client = boto3.client('cognito-idp', region_name='eu-west-1')
    # USER_POOL_ID = 'eu-west-1_zKGLIBXYH'
    # CLIENT_ID = '48nhuo85q76h6l3to96rf8f80m'

    AWS_ACCESS_KEY = 'AKIAW5BFWO2AKMY5FNMW'
    AWS_SECRET_KEY = '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'
    REGION_NAME = 'eu-west-1'
    BUCKET_NAME = 'signin-storage'
    DYNAMODB_TABLE_NAME = 'users'

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    

    # Upload image to S3
    try:
        s3.upload_fileobj(file, BUCKET_NAME, uniqueName)
        # Store reference in DynamoDB
        image_reference = {
            'ImageID': str(uuid.uuid4()),
            'S3URL': f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{uniqueName}",
            'Filename': uniqueName
        }
        table.put_item(Item=image_reference)

        returnStr = jsonify(image_reference)
        code = 200

    except Exception as e:
        log.warning('<-------------Exception occurred--------->'+str(e))
        returnStr = 'Error occured'
        code = 500

    return returnStr,code




def compare(imgFile, username):

    log.warning('<----------------Inside SignUp compare----------------->')

    AWS_ACCESS_KEY = 'AKIAW5BFWO2AKMY5FNMW'
    AWS_SECRET_KEY = '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'
    REGION_NAME = 'eu-west-1'
    BUCKET_NAME = 'signin-storage'
    DYNAMODB_TABLE_NAME = 'users'

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)
    dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)
    rekognition = boto3.client('rekognition', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)


    unique_filename = str(uuid.uuid4()) + '_' + imgFile.filename

    try:
        # Retrieve the image reference from DynamoDB
        response = table.get_item(Key={'Filename': username})
        if 'Item' not in response:
            return 'Image reference not found in DynamoDB', 404
        saved_image_url = response['Item']['S3URL']



            # Upload the provided image to S3 temporarily for comparison
        s3.upload_fileobj(imgFile, BUCKET_NAME, unique_filename)



            # Use Rekognition to compare the images
        compare_response = rekognition.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': unique_filename
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': username  # Assuming the filename in DynamoDB is the same as in S3
                }
            }
        )               



        # Optionally, delete the temporary image from S3
        #s3.delete_object(Bucket=BUCKET_NAME, Key=unique_filename)

        returnStr = jsonify(compare_response['FaceMatches'])
        code = 200


    except Exception as e:
        log.warning('<------------Error Occurred----------->'+str(e))
        returnStr = 'Error occured'
        code = 500

    return returnStr,code



def AwsRedirect(roleAR):
    log.warning('<----------------Inisde  SignUp  AWSRedirect------------>')

    #  2FA arn:aws:iam::474672952960:role/dev
    #  3FA  arn:aws:iam::474672952960:role/sec 
    sts_client = boto3.client('sts')
    
    # Assume role to get temporary credentials
    assumed_role = sts_client.assume_role(
        #RoleArn=roleAR,
        RoleArn = 'arn:aws:iam::474672952960:role/role_to_access_s3',
        RoleSessionName="ConsoleAccessSession"
    )

    # Get federation token using the assumed role's temporary credentials
    session = {
        "sessionId": assumed_role['Credentials']['AccessKeyId'],
        "sessionKey": assumed_role['Credentials']['SecretAccessKey'],
        "sessionToken": assumed_role['Credentials']['SessionToken']
    }
    
    # Get sign-in token using federation token
    request_parameters = "?Action=getSigninToken"
    request_parameters += "&Session=" + requests.utils.quote(json.dumps(session))
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters

    try:
        response = requests.get(request_url)
        
        sign_in_token = response.json()["SigninToken"]
        
        # Construct login URL
        request_parameters = "?Action=login"
        request_parameters += "&Issuer=requester"
        request_parameters += "&Destination=" + requests.utils.quote("https://console.aws.amazon.com/")
        request_parameters += "&SigninToken=" + sign_in_token
        request_url = "https://signin.aws.amazon.com/federation" + request_parameters

        return (request_url)
    except Exception as e:
        log.warning('<----------------Exception Occured---------->')
        log.warning('Error------>'+str(e))
        return(500)

    return (500)

    #return redirect(request_url, code=302)
        
