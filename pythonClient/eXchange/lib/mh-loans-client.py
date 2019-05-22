import exchange_paginated_api
import sys 
    
'''Our main function -- only gets invoked if this is the "outer"
   Python script invoked.
   Thanks to Tierney Pitzer for this if statement.'''
if __name__ == "__main__":
    if len(sys.argv) == 2:
        output_file_name = sys.argv[1]
    else:
        output_file_name = '-'
        
    MH_LOANS_API = "/v1/manufactured-housing-loans/acquisitions"
    DATA_SET_TYPE = "acquisitions"
    exchange_paginated_api.run(MH_LOANS_API,DATA_SET_TYPE,output_file_name)

