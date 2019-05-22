import string

with open("/tmp/counties.txt","rb") as input_file:
    for line in input_file:
        columns = string.split(line,"|")
        fips_code = columns[0]
        county_name = columns[1].replace("'","''")
        print 'UPDATE counties set county_name = ' + "'" + county_name + "' WHERE fips_code = '" + fips_code + "';"
            
