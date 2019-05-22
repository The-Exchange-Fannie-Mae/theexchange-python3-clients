import requests
import sys
import exchange_client
from exchange_client import smart_open
import json
import os
import tempfile


def log(msg):
    sys.stderr.write(msg + "\n")
    
'''Converts float type to int type and returns the converted value. If error occurrs return original float value'''
def convertFloatToIntType(floatValue):
    convertedValue = -1.0
    isErrored = False
    try:
        convertedValue = int(floatValue)
    except ValueError:
        log(floatValue +" is not a numeric value")
        isErrored = True
    if(not isErrored):
        return convertedValue
    else:
        return floatValue
        
        
        
        
'''Make a request to an eXchange paginated API.
   @Param api_uri String -- API's URI (does not include the "base" URI)
   @Param data_set_type String -- name of the data set type that is fetched via the request
   @Param output_name (optional) -- name of file in which to place output; if None then a file name is generated
   @Return string -- name of output file
'''
def run(api_uri, data_set_type, output_name=None):
    base_uri = "https://api.theexchange.fanniemae.com"
    #use the exchange_client to get our access token
    full_auth = exchange_client.get_auth_token()
    user_token = full_auth["AuthenticationResult"]["IdToken"]   
    uri = base_uri + api_uri
    page_num=0
    all_pages_read = False
    total_pages = get_page_count(data_set_type,uri, user_token)
    log("total pages:  " + str(total_pages))
    if output_name is None or output_name == '-':
        log("sending output to stdout")
        output_file_name = '-'
    else:
        log("sending output to " + output_name)
        output_file_name = output_name
            
    with smart_open(output_file_name) as output_file:
        output_file.write('{\n"acquisitions": [')
        for page_num in range(total_pages):
            log("getting page " + str(page_num) + " of " + str(total_pages))
            response = get_page(uri,page_num,user_token)
            as_string = response.json()
            good_parts = as_string["_embedded"][data_set_type]
            for memberIdx in range(len(good_parts)):
                one_acq = good_parts[memberIdx]
                '''Check if the key exists in the dictionary. If it exists convert its value type to int type'''
                if 'originalUnpaidPrincipalBalance' in one_acq:
                    one_acq['originalUnpaidPrincipalBalance'] = convertFloatToIntType(one_acq['originalUnpaidPrincipalBalance'])
                if 'originalLoanTerm' in one_acq:
                    one_acq['originalLoanTerm'] = convertFloatToIntType(one_acq['originalLoanTerm'])
                if 'originalLoanToValue' in one_acq:
                    one_acq['originalLoanToValue'] = convertFloatToIntType(one_acq['originalLoanToValue'])
                if 'originalCombinedLoanToValue' in one_acq:
                    one_acq['originalCombinedLoanToValue'] = convertFloatToIntType(one_acq['originalCombinedLoanToValue'])
                if 'numberOfBorrowers' in one_acq:
                    one_acq['numberOfBorrowers'] = convertFloatToIntType(one_acq['numberOfBorrowers'])
                if 'debtToIncomeRatio' in one_acq:
                    one_acq['debtToIncomeRatio'] = convertFloatToIntType(one_acq['debtToIncomeRatio'])
                if 'mortgageInsurancePercentage' in one_acq:
                    one_acq['mortgageInsurancePercentage'] = convertFloatToIntType(one_acq['mortgageInsurancePercentage'])
                json.dump(one_acq,output_file,indent=2)
                #special logic for commas only applies to last page
                if (page_num == total_pages -1):
                    if (memberIdx != len(good_parts) -1):
                        output_file.write(',\n')
                else:
                    output_file.write(',')
        #end of for page_num in loop
        output_file.write(']}')
    return output_name
'''---------------------------------------------------------------------------'''

'''Request page_num's content from uri, return as a response object.'''
def get_page(uri, page_num, user_token):
    r = requests.get(uri + "?page=" + str(page_num),headers={"Authorization": user_token, "Accept": "application/json"})
    if r.status_code != 200:
        raise Exception(uri + " resulted in an HTTP " + str(r.status_code))
    return r

'''Determine the total number of pages of output to expect for a
   given API call.  Return an int containing the number of pages.'''
def get_page_count(data_set_type, api_uri, user_token):
    tmp_page_file = tempfile.NamedTemporaryFile(mode='w+b', suffix='.json', prefix='eXchange-'+data_set_type+'-',delete=False)
    tmp_page_file_name = tmp_page_file.name
    r = get_page(api_uri, 0, user_token)
    write_page_to_file_in_chunks(tmp_page_file,r);
    with open(tmp_page_file_name, 'r') as response_file:
        full_response = json.load(response_file)
        total_pages = full_response["total"]
    try:
        os.remove(tmp_page_file_name)
    except OSError:
        pass
    return int(total_pages)

'''Append a response to a file by decomposing the response into chunks
   and writing each chunk to the file.'''
def write_page_to_file_in_chunks(file_handle, r):
    with file_handle:
        chunk_num = 0
        for chunk in r.iter_content(chunk_size=16384):
            file_handle.write(chunk)
            chunk_num+=1
        return chunk_num