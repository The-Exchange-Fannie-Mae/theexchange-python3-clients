import requests
import sys
import json
import exchange_client
from exchange_client import smart_open

#make sure the user passed in a state and a county name

if(len(sys.argv) < 3):
    sys.exit("usage:  python " + sys.argv[0] + " two-letter-state-abbreviation county-name [output-file-name | - ]")
if(len(sys.argv) == 4):
    output_file_name = sys.argv[3]
else:
    output_file_name = '-'

state_abbrev = sys.argv[1]
county_name = sys.argv[2]

#use the exchange_client to get our access token
full_auth = exchange_client.get_auth_token()
user_token = full_auth["AuthenticationResult"]["IdToken"]

base_uri = "https://api.theexchange.fanniemae.com"
loan_limits_api = "/v1/loan-limits/state/"
loan_limits_request = loan_limits_api + state_abbrev + "/county/" + county_name

r = requests.get(base_uri + loan_limits_request,headers={"Authorization": user_token, "Accept": "application/json"})
if r.status_code != 200:
    raise Exception(str(r.status_code) + " HTTP status returned")
else:
    with smart_open(output_file_name) as output_file:
        json_resp = r.json()
        json.dump(json_resp,output_file,indent=2,ensure_ascii=False)
    
