from licensing.models import *
from licensing.methods import Key, Helpers

RSAPubKey = "<RSAKeyValue><Modulus>1HAZCDeoW9Nv6c4J4vBUKuhVlztYSkWzPMJSI71f8M6syJj7hya8BwhNWYSqENm9FPVS0HnAz74aMlHGnCo4NpLaRTVbh0dTwXwv6k4Brxt8FicZ8YxJ1VaqKccdsHVqULIkMWTMrYU/D4XNGBAKaKZ/fhmkv1yj/c9siOl/VJbbD0ULZs1wipMXkSJwtdCaeTjDwMAi8s/jIj/2T0etCga/2H/2ba6Cz5biOvM+MXl9om7HhcdIdeviaCxfvIGf/94GgHECiSu/3+41cDh8xPZuzQ2z2VLEGFaaB+mHgi9bG4ZMzZYtKfwLa+O7ePQuTktASj9N1ZTGHzJA/mwatw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI3MTA1ODEzNiIsImREaDFvdEFUbDhheHJSdDQ3anFlNGhvaHZwTTlIRndRR1Q1YkE2OGciXQ=="
global activation
result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=23393, \
                   key="BUBGT-POTQS-HBETT-JQNTP",\
                   machine_code=Helpers.GetMachineCode(v=2))
#if result[0] == None:
if result[0] == None or not Helpers.IsOnRightMachine(result[0], v=2):
    activation = False
    print("The license does not work: {0}".format(result[1]))
else:
    activation = True
    print("The license is valid!")
    license_key = result[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))

print(activation)
