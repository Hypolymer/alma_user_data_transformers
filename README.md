# Alma User Data Transformer Python

This repository was created to store three different types of data transformers.  There is one transformer for each file type:
* .plif
* .csv
* .xml

The structure of the user XML (with sample values):

```
  user_xml = ('<user>' +
             '<record_type desc="Public">PUBLIC</record_type>' +
             '<primary_id>' + str(line[1003:1018]).strip() + '</primary_id>' +            
             '<first_name>' + firstname + '</first_name>' +
             '<last_name>' + lastname + '</last_name>' +
             '<full_name>' + str(line[1305:1354]).strip() + '</full_name>' +
             '<user_group desc="' + patron_type_text + '">' + patron_type + '</user_group>' +                                                        
             '<birth_date>' + the_birth_date +'</birth_date>' +                                   
             '<expiry_date>' + the_expiry_date + '</expiry_date>' +
             '<purge_date>' + the_expiry_date + '</purge_date>' +            
             '<status desc="Active">ACTIVE</status>' +
             '<contact_info>' +
             '<addresses>' +
             '<address preferred="true" segment_type="Internal">' +
             '<line1>' + str(line[1354:1404]).strip() + '</line1>' +
             '<line2>' + str(line[1504:1554]).strip() + '</line2>' +
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
             '</user_identifiers>' +
             '</user>')
```
