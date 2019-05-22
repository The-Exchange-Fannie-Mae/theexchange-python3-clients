import base64
import boto3
import hmac
import hashlib
import json
import os
import sys
import contextlib

'''primary public entrypoint to this module --
   given a valid eXchange-client.properties file located in
   $EXCHANGE_CLIENT_HOME (or %%EXCHANGE_CLIENT_HOME%% if you are
   a command-prompt person), this function returns a valid
   Authorization Token that can be used to make eXchange API calls. '''
def get_auth_token():
    client_properties = load_properties()
    secret_str = client_properties["client-secret"]
    secret_bytes = to_byte_array(secret_str)
    client_id_str = client_properties["client-id"]
    client_id_bytes = to_byte_array(client_id_str)
    user_name = client_properties["user-name"]
    password = client_properties["password"]
    msg_bytes = to_byte_array(user_name + client_id_str)
    hmac_value = getHmac(secret_bytes, msg_bytes)
    return cognito_auth(hmac_value, client_id_str, user_name, password)

''' Load client properties from
    $EXCHANGE_CLIENT_HOME/eXchange-client.properties.'''
def load_properties():
    #get the eXchange client home directory name or die trying
    home_directory_name = "C:\\Users\\r0ukcb\\pythonClient\\eXchange"
    # if home_directory_name == None:
    #     user_home = os.environ.get('USERPROFILE')
    #     if user_home == None:
    #         raise Exception("neither EXCHANGE_CLIENT_HOME nor USERPROFILE defined, cannot read client properties and therefore cannot proceed")
    #     home_directory_name = user_home + "/eXchange"
    properties_file_name = "eXchange-client.properties"
    properties_file_path = home_directory_name + "/" + properties_file_name
    #open and load the contents of eXchange-client.properties, or die trying
    with open(properties_file_path) as propFile:
        return json.load(propFile)

''' Convenience function to convert a string to a byte array. '''
def to_byte_array(string_value):
    new_bytes = bytearray()
    new_bytes.extend(string_value.encode())
    return new_bytes

'''Given an HMAC hash, a Cognito client ID, and a userName/password known
   to the designated Cognito client, authenicate the user and return an
   authorization token.  '''
def cognito_auth(hmac_value, client_id, user_name, password):
    client = boto3.client('cognito-idp','us-east-1')
    auth_parameters = {"USERNAME": user_name, "PASSWORD": password, "SECRET_HASH": hmac_value}
    resp = client.initiate_auth(ClientId=client_id,AuthFlow="USER_PASSWORD_AUTH", AuthParameters=auth_parameters)
    return resp

'''Generate an HMAC256 key to pass to cognito'''
def getHmac(secret_bytes, msg_bytes):
    dig = hmac.new(secret_bytes, msg_bytes, digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()      


'''A simple helper to generate a temp file name.
   The file name will be ${tmpDir}/prefix${PID}suffix'''
def tmpFileName(prefix, suffix, tmpDir=''):
    if tmpDir == '':
        if not 'TMP' in os.environ:
            raise Exception("no temp directory specified as $TMP or %%TMP%%")
        tmpDir=os.environ['TMP']
    return tmpDir+"/"+prefix+ str(os.getpid()) + suffix

'''Thanks to https://stackoverflow.com/a/17603000/3839108 for this function.
   This function allows us to open either a named file or stdout in the
   context of a with block.'''
@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

'''If run directly from this module (as opposed to this module being imported
   into another module), then the following lines are executed; this is
   basically our equivalent of a java public static void main '''
if __name__ == "__main__":
    cognito_response = get_auth_token()
    id_token = cognito_response["AuthenticationResult"]["IdToken"]
    with smart_open('-') as output:
        output.write(id_token+"\n")

