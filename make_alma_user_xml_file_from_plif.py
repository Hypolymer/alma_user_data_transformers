# This python script is used to take a plif file with user information and transform it into XML for Ex Libris Alma
# The plif file is a flat file and each field has a specific amount of character space it can have, and each row in the file is a patron
# In the variables below, a line like str(line[133:333]) means that python grabs character position 133 through 332 (position 333 is the stopping point).  
#
# Author:  Bill Jones (jonesw@geneseo.edu)
#
# License:  CC BY-NC-SA
#
# Pages that helped:
# https://stackabuse.com/read-a-file-line-by-line-in-python/
# https://www.datacamp.com/community/tutorials/reading-writing-files-python
# https://stackoverflow.com/questions/7152762/how-to-redirect-print-output-to-a-file-using-python
#
#
#
# If you run into problems, be sure to open the plif and save it as UTF-8 in UltraEdit

import sys  
import os
import zipfile
from datetime import datetime
today = datetime.today().strftime('%Y%m%d' + '_' + '%H%M%S')

# These are the variables you type with the command:  python makealmaplif.py plif_file.plif
###################################################:  python nameofscript    patron file to read
input_path = sys.argv[1]
output_file = 'Alma_patron_XML_' + today + ".xml"

# Set up counter
x=0

my_file=open(input_path,"r")
new_file=open(output_file,mode="w")
user_write_out = ""

for line in my_file:

  # This is to split the comma separated last name, first name into individual 'first name' and 'last name' variables
  # https://stackoverflow.com/questions/27299404/python-string-get-leading-characters-up-to-first-comma
  strIn = str(line[133:333]).strip()
  str_list = strIn.split(',')
  lastname = str_list[0]
  lastname = lastname.strip()
  firstname = str_list[1]
  firstname = firstname.strip()
  
  # This is to get the first part of the email address
  # This has been commented out for testing  20190607
  # webusername = str(line[1684:1744]).strip()
  # webusername = webusername.split("@")[0]
  
  # This is to get the correct user type (Student, Faculty, Staff)
  patron_type = str(line[1001:1003]).strip()
  patron_type_text = ""
  if patron_type == "01":
        patron_type_text = "Student"
  if patron_type == "30":
    patron_type_text = "Library Staff"
  if patron_type == "31":
    patron_type_text = "Faculty/Staff/Administration"
  if patron_type == "32":
    patron_type_text = "Adjunct Faculty"
  if patron_type == "46":
    patron_type_text = "In-House Use"
  if patron_type == "55":
    patron_type_text = "Bad Patron"
  if patron_type == "56":
    patron_type_text = "InterLibrary Loan"
  if patron_type == "60":
    patron_type_text = "Community User"
  if patron_type == "61":
    patron_type_text = "Community - Upward Bound"
  if patron_type == "79":
    patron_type_text = "JUNK"
  if patron_type == "80":
    patron_type_text = "SUNY Open Access"

  birth_year = str(line[333:337]).strip()
  birth_day = str(line[339:341]).strip()
  birth_month = str(line[337:339]).strip()
  the_birth_date = birth_year + "-" + birth_month + "-" + birth_day + "Z"

  expiry_year = str(line[1810:1814]).strip()
  expiry_day = str(line[1816:1818]).strip()
  expiry_month = str(line[1814:1816]).strip()
  the_expiry_date = expiry_year + "-" + expiry_month + "-" + expiry_day + "Z"
             
  user_xml = ('<user>' +
             '<record_type desc="Public">PUBLIC</record_type>' +
             '<primary_id>' + str(line[1003:1018]).strip() + '</primary_id>' +            
             '<first_name>' + firstname + '</first_name>' +
             '<last_name>' + lastname + '</last_name>' +
             '<full_name>' + str(line[1305:1354]).strip() + '</full_name>' +
             #'<pin_number></pin_number>' +
             '<user_group desc="' + patron_type_text + '">' + patron_type + '</user_group>' +                                                        
             '<birth_date>' + the_birth_date +'</birth_date>' +                                   
             '<expiry_date>' + the_expiry_date + '</expiry_date>' +
             '<purge_date>' + the_expiry_date + '</purge_date>' +            
             #'<account_type desc="Internal">INTERNAL</account_type>' +
             #'<external_id></external_id>' +
             #'<password></password>' +
             #'<force_password_change></force_password_change>' +
             '<status desc="Active">ACTIVE</status>' +
             '<contact_info>' +
             '<addresses>' +
             '<address preferred="true" segment_type="Internal">' +
             '<line1>' + str(line[1354:1404]).strip() + '</line1>' +
             '<line2>' + str(line[1504:1554]).strip() + '</line2>' +
             #'<city></city>' +
             #'<state_province></state_province>' +
             '<postal_code>' + str(line[1554:1563]).strip() + '</postal_code>' +
             '<country desc=""></country>' +
             '<address_note>User Address Type: Permanent address</address_note>' +
             '<address_types><address_type desc="Home">home</address_type>' +
             '</address_types>' +
             '</address>' +
             '</addresses>' +
             '<emails>' +
             '<email preferred="true" segment_type="Internal">' +
             '<email_address>' + str(line[1684:1744]).strip() + '</email_address>' +
             '<email_types>' +
             '<email_type desc="Personal">personal</email_type>' +
             '</email_types>' +
             '</email>' +
             '</emails>' +
             '<phones>' +
             '<phone preferred="true" preferred_sms="false" segment_type="Internal">' +
             '<phone_number>' + str(line[1564:1594]).strip() + '</phone_number>' +
             '<phone_types>' +
             '<phone_type desc="Home">home</phone_type>' +
             '</phone_types>' +
             '</phone>' +
             '</phones>' +
             '</contact_info>' +
             #'<pref_first_name></pref_first_name>' +
             #'<pref_middle_name></pref_middle_name>' +
             #'<pref_last_name></pref_last_name>' +
             '<user_identifiers>' +
             '<user_identifier>' +
             '<id_type desc="Power Campus ID">99</id_type>' + 
             '<value>' + str(line[3:23]).strip() + '</value>' +
             '<status>ACTIVE</status>' +
             '</user_identifier>' +
             '<user_identifier segment_type="External">' +
             '<id_type desc="WEB Access">02</id_type>' +            
             '<value>' + str(line[1684:1744]).strip() + '</value>' +           
             '<status>ACTIVE</status>' +
             '</user_identifier>' +
             #'<user_identifier segment_type="External">' +
             #'<id_type desc="Login">03</id_type>' +            
             #'<value>' + str(line[1684:1744]).strip() + '</value>' +           
             #'<status>ACTIVE</status>' +
             #'</user_identifier>' +
             '</user_identifiers>' +
             '</user>')
  user_write_out = user_write_out + user_xml
  x = x + 1
new_file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Users>' + user_write_out + '</Users>')
new_file.close()

#https://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/zipfile/index.html
import zipfile
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
print "You just completed processing " + place_value(x) + " patron records"
print "A .zip file has been created with the filename: " + zip_filename
print "The .zip file is ready to be uploaded to the Alma SFTP server"

# Map of the PLIF fields read from FMCC .plif file using the Help File:  plif_help-file-20_specs_flatfile-1
#   
#              "<USER-REC-MATCH-ID>" + str(line[3:23]).strip() + "</USER-REC-MATCH-ID>" +
#              "<USER-REC-ID-1>" + str(line[23:43]).strip() + "</USER-REC-ID-1>" +
#              "<USER-REC-ID-2>" + str(line[43:63]).strip() + "</USER-REC-ID-2>" +
#              "<USER-REC-VERIFICATION-1>" + str(line[63:83]).strip() + "</USER-REC-VERIFICATION-1>" +
#              "<USER-REC-VERIFICATION-2>" + str(line[83:103]).strip() + "</USER-REC-VERIFICATION-2>" +
#              "<USER-REC-VERIFICATION-3>" + str(line[103:123]).strip() + "</USER-REC-VERIFICATION-3>" +
#              "<USER-REC-NAME-TITLE>" + str(line[123:133]).strip() + "</USER-REC-NAME-TITLE>" +
#              "<USER-REC-NAME>" + str(line[133:333]).strip() + "</USER-REC-NAME>" +
#              "<USER-REC-BIRTH-DATE>" + str(line[333:341]).strip() + "</USER-REC-BIRTH-DATE>" +
#              "<USER-REC-BUDGET>" + str(line[341:361]).strip() + "</USER-REC-BUDGET>" +
#              "<USER-REC-EXPORT-CONSENT>" + str(line[361:362]).strip() + "</USER-REC-EXPORT-CONSENT>" +
#              "<USER-REC-DELINQ-INDEX>" + str(line[362:363]).strip() + "</USER-REC-DELINQ-INDEX>" +
#              "<USER-REC-DELINQ>" + str(line[363:365]).strip() + "</USER-REC-DELINQ>" +
#              "<USER-REC-DELINQ-N>" + str(line[365:565]).strip() + "</USER-REC-DELINQ-N>" +
#              "<USER-REC-FIELD-INDEX>" + str(line[565:566]).strip() + "</USER-REC-FIELD-INDEX>" +
#              "<USER-REC-FIELD>" + str(line[566:766]).strip() + "</USER-REC-FIELD>" +
#              "<USER-REC-PROFILE-ID>" + str(line[766:778]).strip() + "</USER-REC-PROFILE-ID>" +
#              "<USER-REC-ILL-LIBRARY>" + str(line[778:783]).strip() + "</USER-REC-ILL-LIBRARY>" +
#              "<USER-REC-HOME-LIBRARY>" + str(line[783:788]).strip() + "</USER-REC-HOME-LIBRARY>" +
#              "<USER-REC-ILL-TOTAL-LIMIT>" + str(line[788:792]).strip() + "</USER-REC-ILL-TOTAL-LIMIT>" +
#              "<USER-REC-ILL-ACTIVE-LIMIT>" + str(line[792:796]).strip() + "</USER-REC-ILL-ACTIVE-LIMIT>" +
#              "<USER-REC-SEND-ALL-LETT>" + str(line[796:797]).strip() + "</USER-REC-SEND-ALL-LETT>" +
#              "<USER-REC-PROXY-FOR-ID>" + str(line[797:809]).strip() + "</USER-REC-PROXY-FOR-ID>" +
#              "<USER-REC-PRIMARY-ID>" + str(line[809:821]).strip() + "</USER-REC-PRIMARY-ID>" +
#              "<USER-REC-CON-LNG>" + str(line[821:824]).strip() + "</USER-REC-CON-LNG>" +
#              "<USER-REC-TYPE>" + str(line[824:829]).strip() + "</USER-REC-TYPE>" +
#              "<USER-REC-PLAIN-HTML>" + str(line[829:830]).strip() + "</USER-REC-PLAIN-HTML>" +
#              "<USER-REC-WANT-SMS>" + str(line[830:831]).strip() + "</USER-REC-WANT-SMS>" +
#              "<USER-REC-NOTE-INDEX>" + str(line[831:832]).strip() + "</USER-REC-NOTE-INDEX>" +
#              "<USER-REC-NOTE>" + str(line[832:932]).strip() + "</USER-REC-NOTE>" +
#              "<USER-REC-SALUTATION>" + str(line[932:982]).strip() + "</USER-REC-SALUTATION>" +
#              "<USER-REC-TITLE-REQ-LIMIT>" + str(line[982:986]).strip() + "</USER-REC-TITLE-REQ-LIMIT>" +
#              "<FILLER>" + str(line[986:994]).strip() + "</FILLER>" +
#              "<USER-REC-NO-ID>" + str(line[994:996]).strip() + "</USER-REC-NO-ID>" +
#              "<USER-REC-NO-ADDRESS>" + str(line[996:998]).strip() + "</USER-REC-NO-ADDRESS>" +
#              "<USER-REC-NO-BOR>" + str(line[998:1000]).strip() + "</USER-REC-NO-BOR>" +
#              "<LOGIN-REC-ACTION>" + str(line[1000:1001]).strip() + "</LOGIN-REC-ACTION>" +
#              "<LOGIN-REC-TYPE>" + str(line[1001:1003]).strip() + "</LOGIN-REC-TYPE>" +
#              "<LOGIN-REC-LOGIN>" + str(line[1003:1023]).strip() + "</LOGIN-REC-LOGIN>" +
#              "<LOGIN-REC-VERIFICATION>" + str(line[1023:1043]).strip() + "</LOGIN-REC-VERIFICATION>" +
#              "<LOGIN-REC-VERIFICATION-TYPE>" + str(line[1043:1045]).strip() + "</LOGIN-REC-VERIFICATION-TYPE>" +
#              "<LOGIN-REC-STATUS>" + str(line[1045:1047]).strip() + "</LOGIN-REC-STATUS>" +
#              "<LOGIN-REC-ENCRYPTION>" + str(line[1047:1048]).strip() + "</LOGIN-REC-ENCRYPTION>" +
#              "<FILLER>" + str(line[1048:1100]).strip() + "</FILLER>" +
#              "<ADDR-REC-ACTION>" + str(line[1300:1301]).strip() + "</ADDR-REC-ACTION>" +
#              "<ADDR-REC-SEQUENCE>" + str(line[1301:1303]).strip() + "</ADDR-REC-SEQUENCE>" +
#              "<ADDR-REC-TYPE>" + str(line[1303:1305]).strip() + "</ADDR-REC-TYPE>" +
#              "<ADDR-REC-ADDR-1>" + str(line[1305:1354]).strip() + "</ADDR-REC-ADDR-1>" +
#              "<ADDR-REC-ADDR-2>" + str(line[1354:1404]).strip() + "</ADDR-REC-ADDR-2>" +
#              "<ADDR-REC-ADDR-3>" + str(line[1404:1454]).strip() + "</ADDR-REC-ADDR-3>" +
#              "<ADDR-REC-ADDR-4>" + str(line[1454:1504]).strip() + "</ADDR-REC-ADDR-4>" +
#              "<ADDR-REC-ADDR-5>" + str(line[1504:1554]).strip() + "</ADDR-REC-ADDR-5>" +
#              "<ADDR-REC-ZIP>" + str(line[1554:1563]).strip() + "</ADDR-REC-ZIP>" +
#              "<FILLER>" + str(line[1563:1564]).strip() + "</FILLER>" +
#              "<ADDR-REC-PHONE>" + str(line[1564:1594]).strip() + "</ADDR-REC-PHONE>" +
#              "<ADDR-REC-PHONE-2>" + str(line[1594:1624]).strip() + "</ADDR-REC-PHONE-2>" +
#              "<ADDR-REC-PHONE-3>" + str(line[1624:1654]).strip() + "</ADDR-REC-PHONE-3>" +
#              "<ADDR-REC-PHONE-4>" + str(line[1654:1684]).strip() + "</ADDR-REC-PHONE-4>" +
#              "<ADDR-REC-E-MAIL>" + str(line[1684:1744]).strip() + "</ADDR-REC-E-MAIL>" +
#              "<ADDR-REC-START-DATE>" + str(line[1744:1753]).strip() + "</ADDR-REC-START-DATE>" +
#              "<ADDR-REC-STOP-DATE>" + str(line[1753:1761]).strip() + "</ADDR-REC-STOP-DATE>" +
#              "<ADDR-REC-SMS-NUMBER>" + str(line[1761:1791]).strip() + "</ADDR-REC-SMS-NUMBER>" +
#              "<FILLER>" + str(line[1791:1800]).strip() + "</FILLER>" +
#              "<BOR-REC-ACTION>" + str(line[1800:1801]).strip() + "</BOR-REC-ACTION>" +
#              "<BOR-REC-SUB-LIBRARY>" + str(line[1801:1806]).strip() + "</BOR-REC-SUB-LIBRARY>" +
#              "<BOR-REC-TYPE>" + str(line[1806:1808]).strip() + "</BOR-REC-TYPE>" +
#              "<BOR-REC-STATUS>" + str(line[1808:1810]).strip() + "</BOR-REC-STATUS>" +
#              "<BOR-REC-EXPIRY-DATE>" + str(line[1810:1818]).strip() + "</BOR-REC-EXPIRY-DATE>" +
#              "<BOR-REC-REGISTRATION-DATE>" + str(line[1818:1826]).strip() + "</BOR-REC-REGISTRATION-DATE>" +
#              "<FILLER>" + str(line[1826:2000]).strip() + "</FILLER>")
