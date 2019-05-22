# theexchange-python3-clients
theexchange python3 clients, including code samples to authenticate, authorize, submit requests, and process responses both small and large.


### Installation Instructions:

	Step1: Set the EXCHANGE_CLIENT_HOME environment variable to     $HOME/eXchange:
		bash --> export EXCHANGE_CLIENT_HOME=~/eXchange

	Step2: Untar into your home directory.  This will create the following:
		$HOME/.aws/credentials -- the client ID for Cognito access
		$HOME/eXchange
		$HOME/eXchange/lib -- place where the python clients reside
		$HOME/eXchange/eXchange-client.properties -- place for Exchange credentials

	Step3: Make sure you have python3 on your PATH.  I used /appl/tools/R-3.4.3/bin/python3
        •	Make sure you have boto3 installed
        •	Make sure you have set both HTTP_PROXY and HTTPS_PROXY:
		
		export HTTP_PROXY=http://zsproxy.fanniemae.com:10479
		export HTTPS_PROXY=http://zsproxy.fanniemae.com:10479

	Step4: Edit $HOME/eXchange/eXchange-client.properties so it contains your Exchange user ID and password

Always invoke the client with "python3".  






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
