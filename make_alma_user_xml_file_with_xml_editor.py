# Written by Bill Jones, jonesw@geneseo.edu
#
# License:  CC BY-NC-SA
#
# Helpful doc:  https://docs.python.org/3.4/library/xml.etree.elementtree.html

# These import the needed libraries for the project
import sys  
import os
import xml.etree.ElementTree as ET
from datetime import datetime

# This get's todays date so that it can be tacked on to the filename
today = datetime.today().strftime('%Y%m%d' + '_' + '%H%M%S')

# This sets the output filename for the XML document
output_filename = "Alma_XML_user_export_" + today + ".xml"

# This is the variable you type with the command:  python makealmaplif.py users.xml
############################################### :  python nameofscript    xml file to read
input_path = sys.argv[1]

# This sets the Element Tree reader and root of the XML file
tree = ET.parse(input_path)
root = tree.getroot()

#set users without address
no_address = 0
no_email = 0
no_email_user_list = ""

#record iterator counter
x = 0

print ("Process Starting...")

# For each user
for this in root.iter('user'):

  # Locate email_address node to pull email address from
  email_address_node = this.find('.//contact_info/emails/email/email_address')

  # Locate the user_identifiers node to append the email address to 
  user_identifiers_node = this.find('.//user_identifiers')
  
  user_primary_id = this.find('.//primary_id')

  # Locate the address node to set preferred=true  
  address_node = this.find('.//contact_info/addresses/address')
  if address_node is None:
  	no_address = no_address + 1
  else:
    address_node.set('preferred', 'true')

  # Set email_address variable equal to the text of the email_address field  
  if email_address_node is not None:
    email_address = email_address_node.text
  if email_address_node is None:
    no_email = no_email + 1
    no_email_user_list = no_email_user_list + user_primary_id.text + "\r\n"
    email_address = "-"
  #  ET.Element tells python what tag to append the SubElement variables to 
  a = ET.Element("user_identifier")
  
  # myattributes sets the attribtes for the id_type field being added
  myattributes = {"desc": "Library Identifier"}
 
  # This creates the id_type tag with attributes defined above 
  b = ET.SubElement(a, "id_type", attrib=myattributes) 
  
  # This creates the value tag 
  c = ET.SubElement(a, "value")

  # This sets the value for the id_type field to 40
  b.text = "40" 
  
  # This sets the value for the "value" field equal to the user's email address
  c.text = email_address

  # This appends the newly created tags to the user's record, under the unique_identifiers node 
  user_identifiers_node.append(a)
  
  x = x + 1

# This writes the newly created XML to a file  
tree.write(open(output_filename, 'wb'), encoding='UTF-8')

# This is where we create the .zip folder
#https://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/zipfile/index.html
import zipfile
zip_filename = "Alma_XML_user_export_" + today + ".zip"
zf = zipfile.ZipFile(zip_filename, mode='w',compression=zipfile.ZIP_DEFLATED,)
try:
    zf.write(output_filename)
finally:
    zf.close()
    # Erases the XML file that was created to go in the zip folder
    os.remove(output_filename)
 
def place_value(number): 
    return ("{:,}".format(number)) 
print ("#")
print ("#")
print ("#")
print ("Congratulations!")
print ("You just completed processing " + place_value(x) + " patron records")
print ("There were " + place_value(no_address) + " users without a local address.  You might want to check these out.")
print ("There were " + place_value(no_email) + " users without an email address.  You might want to check these out.")
if no_email_user_list is not None:
    print ("Those users were...")
    print (no_email_user_list)
print ("A .zip file has been created with the filename: " + zip_filename)
print ("The .zip file is ready to be uploaded to the Alma SFTP server")

# Uncomment for debugging, and comment out "os.remove(output_filename)"
#trees = ET.parse(output_filename)
#roots = trees.getroot()
#print(ET.tostring(root, encoding='utf8').decode('utf8'))
