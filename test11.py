from validate_email_address import validate_email
import re
import DNS

Email = 'ashloverscn@gmail.com'

def pattern_match(email):
    #pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    pattern = r'^\s*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\s*$'
    return re.match(pattern, email) is not None

def verify_email(email):
    DNS.defaults['server']=['8.8.8.8', '8.8.4.4']
    result = validate_email(email, verify=True)
    return result.is_valid

if pattern_match(Email):
    print("Email address is valid for Pattern method.")    
else:
    print("Email address is invalid for Pattern method.")
if verify_email(Email):
    print("Email address is valid for Verifier Library method.")
else:
    print("Email address is invalid for Verifier Library method.")
    
input() 
