
# theexchange-python3-clients
theexchange python3 clients, including code samples to authenticate, authorize, submit requests, and process responses both small and large.


### Installation Instructions:

	Step1: Create a directory into which you can clone this repo; that directory's name will become the value for
	the EXCHANGE_CLIENT_HOME environment variable.  This document will use $HOME/eXchange as the example name of 
	this directory.
	
	Step2:  Set the EXCHANGE_CLIENT_HOME environment variable to $HOME/eXchange and cd into that directory:
		bash--> export EXCHANGE_CLIENT_HOME=$HOME/eXchange
		bash--> cd $EXCHANGE_CLIENT_HOME

	Step3: Use git clone to obtain the client code and config files 

	Step4: Make sure you have boto3 installed (so you can interact with AWS Cognito and obtain AUTH tokens):	

	Step5: Edit $HOME/eXchange/eXchange-client.properties so it contains your Exchange user ID and password

	Step6:  Run a smoke test; if successful it will display an AUTH token:
		bash--> python exchange_client.py


| Base Modules | Description |
| --- | --- |
| exchange_client.py | Sample code to get auth tokens plus a few ancillary functions.If run directly from the command line, 				exchange_client.py fetches and displays an auth token to stdout. |
| exchange_paginated_api.py | Sample code that handles simple non-paginated API calls. For example, nhs_client.py delegates much of its work to exchange_nonpaginated_api.py. |
| exchange_nonpaginated_api.py | Sample code that handles simple non-paginated API calls. For example, nhs_client.py delegates much of its work to exchange_nonpaginated_api.py. |



| Concrete Clients | Description |
| --- | --- |
| loan-limits-client.py | Given a two-character state abbreviation and a county name, retrieves the loan limits in place for that county; for example, try python3 loan-limits-client.py MT 'Missoula County'|
| mh-communities-count-client.py | Creates a file named /tmp/mhc-counts.json containing a state-by-state count of manufactured housing communities (as reported by Reonomy). |
| mh-communities-nationwide-aggregations-client.py | Creates a file named /tmp/mhc-nationwide-communities-count.json that contains the total count of MHCs across the nation.|
| mh-loans-client.py | Uses the exchange_paginated_client to retrieve all MH loans and write them to an output file (defaults to stdout, specify an output file name on the command line to have it write the output elsewhere). |
| nhs-client.py| Retrieves the most recent NHS results and writes them as JSON to either stdout (default) or a specific file if a file name is passed in from the command line.|



### License Summary
This sample code is made available under the MIT-0 license. See the LICENSE file.
