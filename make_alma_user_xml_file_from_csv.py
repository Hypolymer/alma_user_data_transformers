# This python script is used to take a csv file with user information and transform it into XML for Ex Libris Alma
# This script was originally built for SUNY Optometry
#
# Author:  Bill Jones (jonesw@geneseo.edu)
# License:  CC BY-NC-SA
# September 1, 2019
#
# Pages that helped:
# https://stackabuse.com/read-a-file-line-by-line-in-python/
# https://www.datacamp.com/community/tutorials/reading-writing-files-python
# https://stackoverflow.com/questions/7152762/how-to-redirect-print-output-to-a-file-using-python
# https://stackoverflow.com/questions/14674275/skip-first-linefield-in-loop-using-csv-file
# https://stackoverflow.com/questions/17528374/python-convert-set-to-string-and-vice-versa
# https://realpython.com/python-csv/

import sys  
import os
import csv
import zipfile
from datetime import datetime
today = datetime.today().strftime('%Y%m%d' + '_' + '%H%M%S')


# These are the variables you type with the command:  python make_alma_user_xml_file_from_csv.py patron_file.csv
###################################################:  python nameofscript                        patron file to read
input_path = sys.argv[1]
output_file = 'Alma_patron_XML_' + today + ".xml"

# Set empty values for variables
patron_type_text = ""
patron_type_number = ""
expiry_date = ""
expiry_month = ""
expiry_day = ""
expiry_year = ""
purge_date = ""
purge_month = ""
purge_day = ""
purge_year = ""

new_file=open(output_file,mode="w")
user_write_out = ""

with open(input_path,'rU') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
    	#Check to see if it's the first line, if so, skip to next line
        if line_count == 0:
    	    line_count += 1	
    	    continue
    	#If the line is the second line (or greater, continue to loop)
        if line_count >= 1:
      #First, start building the expiry date.  The date doesn't come formatted how Alma wants it.  Build it.
        	if ''.join({row[3]}) != "":
        		str_list = ''.join({row[3]}).split('/')
        		expiry_month = str_list[0]
        		expiry_day = str_list[1]
       #The year needs to be four digits (e.g., 2019)
        		expiry_year = str_list[2]
        		if int(expiry_month) < 10:
        		 expiry_month = "0" +  expiry_month
        		if int(expiry_day) < 10:
        			expiry_day = "0" +  expiry_day
        		expiry_date = expiry_year + "-" + expiry_month + "-" + expiry_day + "Z"
       #Next, build the purge date.  The date doesn't come formatted how Alma wants it.  Build it.
        	if ''.join({row[4]}) != "":
        		str_list = ''.join({row[4]}).split('/')
        		purge_month = str_list[0]
        		purge_day = str_list[1]
        		purge_year = str_list[2]
        		if int(purge_month) < 10:
        		 purge_month = "0" +  purge_month
        		if int(purge_day) < 10:
        			purge_day = "0" +  purge_day
        		purge_date = purge_year + "-" + purge_month + "-" + purge_day + "Z" 
        #There is a space on either side of the dash for the patron type.  Remove it:
        #We decided that the spreadsheet can have a space on either side of the dash for the patron type
        #The code below will format the patron type description for the XML, and apply the patron type number   			
        	if ''.join({row[2]}) == "Student - Optometry":
        		patron_type_text = "Student-Optometry"
        		patron_type_number = "10"
        	if ''.join({row[2]}) == "Student - Master Candidate":
        		patron_type_text = "Student-Master Candidate"
        		patron_type_number = "11"
        	if ''.join({row[2]}) == "Student Ph.D. Candidate":
        		patron_type_text = "Student Ph.D. Candidate"
        		patron_type_number = "12"
        	if ''.join({row[2]}) == "Student Alumni":
        		patron_type_text = "Student Alumni"
        		patron_type_number = "14"
        	if ''.join({row[2]}) == "Faculty Ful  Time":
        		patron_type_text = "Faculty Full Time"
        		patron_type_number = "30"
        	if ''.join({row[2]}) == "Faculty Full Time":
        		patron_type_text = "Faculty Full Time"
        		patron_type_number = "30"
        	if ''.join({row[2]}) == "Faculty Part Time":
        		patron_type_text = "Faculty Part Time"
        		patron_type_number = "31"
        	if ''.join({row[2]}) == "Faculty Adjunct":
        		patron_type_text = "Faculty Adjunct"
        		patron_type_number = "32"
        	if ''.join({row[2]}) == "Faculty Residents":
        		patron_type_text = "Faculty Residents"
        		patron_type_number = "33"
        	if ''.join({row[2]}) == "Faculty Retired":
        		patron_type_text = "Faculty Retired"
        		patron_type_number = "34"
        	if ''.join({row[2]}) == "Staff":
        		patron_type_text = "Staff"
        		patron_type_number = "40"
        	if ''.join({row[2]}) == "Temporary Patron":
        		patron_type_text = "Temporary Patron"
        		patron_type_number = "56"
        	if ''.join({row[2]}) == "Inter-library Loan":
        		patron_type_text = "Inter-library Loan"
        		patron_type_number = "60"
        	if ''.join({row[2]}) == "Open Access Undergraduate":
        		patron_type_text = "Open Access Undergraduate"
        		patron_type_number = "80"
        	if ''.join({row[2]}) == "Open Access Graduate":
        		patron_type_text = "Open Access Graduate"
        		patron_type_number = "81"
        	if ''.join({row[2]}) == "Open Access Faculty":
        		patron_type_text = "Open Access Faculty"
        		patron_type_number = "82"        		        		        		       		        		        		       		        		        		     		      		       		        		      		     		
        #This is the output template for the Alma user XML
        	user_xml = ('<user>' +
             '<primary_id>' + ''.join({row[5]}) + '</primary_id>' +            
             '<first_name>' + ''.join({row[1]}) + '</first_name>' +
             '<last_name>' + ''.join({row[0]}) + '</last_name>' +
             '<user_group desc="' + patron_type_text + '">' + patron_type_number + '</user_group>' +
             '<preferred_language>en</preferred_language>' +
             '<expiry_date>' + expiry_date + '</expiry_date>' +                  
             '<purge_date>' + purge_date + '</purge_date>' +
             '<status desc="Active">ACTIVE</status>' +         
             '<contact_info>' +
             '<emails>' +
             '<email preferred="true">' +
             '<email_address>' + ''.join({row[6]}) + '</email_address>' +
             '<email_types>' +
             '<email_type desc="School">school</email_type>' +
             '</email_types>' +
             '</email>' +
             '</emails>' +
             '<phones/>' +
             '</contact_info>' +
             '<user_identifiers>' +
             '<user_identifier>' +
             '<id_type desc="Additional">02</id_type>' + 
             '<value>' + ''.join({row[7]}) + '</value>' +
             '</user_identifier>' +
             '</user_identifiers>' +
             '</user>')
        #Count each line that was parsed to get total count of rows processed
        line_count += 1
        #Concatenate all of the user XML blocks together
        user_write_out = user_write_out + user_xml
            
#Do one single write to an XML file and close it before zipping it up
new_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Users>' + user_write_out + '</Users>')
new_file.close()


#https://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/zipfile/index.html
zip_filename = "Alma_XML_user_export_" + today + ".zip"
zf = zipfile.ZipFile(zip_filename, mode='w',compression=zipfile.ZIP_DEFLATED,)
try:
    zf.write(output_file)
finally:
    zf.close()
    # Erases the XML file that was created to go in the zip folder
    os.remove(output_file)
def place_value(number): 
    return ("{:,}".format(number)) 
print "#"
print "#"
print "#"
print "Congratulations!"
print "You just completed processing " + place_value(line_count) + " patron records"
print "A .zip file has been created with the filename: " + zip_filename
print "The .zip file is ready to be uploaded to the Alma SFTP server"
