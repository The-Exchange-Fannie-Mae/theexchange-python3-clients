import exchange_nonpaginated_api
 
    
'''Our main function -- only gets invoked if this is the "outer"
   Python script invoked.
   Thanks to Tierney Pitzer for this if statement.'''
if __name__ == "__main__":  
    MH_COMMS_API = "/v1/manufactured-housing-communities/nation/aggregations"
    output_file_name = exchange_nonpaginated_api.run(MH_COMMS_API,'/tmp/mhc-nationwide-aggregations.json')
