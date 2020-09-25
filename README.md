# Alma User Data Transformer Python

This repository was created to store python scripts that can transform patron data from external Student Information Systems into Alma-compliant XML so that it can be uploaded into Alma.  There is one transformer for each file type:
* [.plif](https://github.com/Hypolymer/alma_user_data_transformers/blob/master/make_alma_user_xml_file_from_plif.py)
* [.csv](https://github.com/Hypolymer/alma_user_data_transformers/blob/master/make_alma_user_xml_file_from_csv.py)
* [.xml](https://github.com/Hypolymer/alma_user_data_transformers/blob/master/make_alma_user_xml_file_with_xml_editor.py)

The files will need to be changed depending on your situation:

In the [.plif](https://github.com/Hypolymer/alma_user_data_transformers/blob/master/make_alma_user_xml_file_from_plif.py) file:
* Change the text values for the "patron_type_text" variables to their correct number/user-label pair from your Aleph.
* In line 140, [```'<id_type desc="Power Campus ID">99</id_type>' + ```], you will probably have a different value for "desc"

In the [.csv](https://github.com/Hypolymer/alma_user_data_transformers/blob/master/make_alma_user_xml_file_from_csv.py) file:
* The .csv file that was used had headings in this order:
  * Last Name
  * First Name

The minimal XML structure for the user (with sample values):

```
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
```
