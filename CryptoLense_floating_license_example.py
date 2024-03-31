from licensing.models import *
from licensing.methods import Key, Helpers
import time

RSAPubKey = "<RSAKeyValue><Modulus>tb4Dkt6rKhnkMt12EwOx/M9Woa+MRSjgkNXqSpA9zzH7KntfNUuCypQuZ1z7kbLhvJ/gXaJCBt/n4j3Ji7TfT8h4OmR1DIjY9OgtUDYFD9zU73rLzdnIgFsS/3S3Rls0Ub1soUnE7eBkp2ikRzTOlm4N0pkC5Y7adBJdmHYTCPiyWyUd3wOKgIB04MDxPZH+Dcdk5kzsieMhuhzlmfJ2T1BUlV6EoPrjhcDcCXkYSPQCJy7bKHx2YPT4KlSK6DkaDf+XC/ngmUR+b8rLdlTmHomcyWAdz5F7jPTbHKspBlro7QXJflnY+tGjY105WgKofh2oB26TTL9AXFBwelWmQw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI3NzIzMDg5MyIsInY5UEUyWW56QVdVbmFHNkpvbXF3NjFlRXo4YlFtdnkyaC8vMjhGd2UiXQ=="
key = "JRLFQ-IRYBO-DDQZQ-MTDGB"
product_id=24509
floating_time_interval=8
max_overdraft=1
global activation
result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=product_id, \
                   key=key,\
                   machine_code=Helpers.GetMachineCode(v=2),\
                   floating_time_interval=floating_time_interval,\
                   max_overdraft=max_overdraft)
activation_time = time.time()
def activation_recheck():
    result = Key.activate(token=auth,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=product_id, \
                   key=key,\
                   machine_code=Helpers.GetMachineCode(v=2),\
                   floating_time_interval=floating_time_interval,\
                   max_overdraft=max_overdraft)
#if result[0] == None:
if result[0] == None or not Helpers.IsOnRightMachine(result[0], is_floating_license=True, allow_overdraft=True, v=2):
    activation = False
    print("The license does not work: {0}".format(result[1]))
else:
    activation = True
    print("The license is valid!")
    license_key = result[0]
    print("Feature 1: " + str(license_key.f1))
    print("License expires: " + str(license_key.expires))

print(activation)

while(1):
    if(time.time() >= activation_time + floating_time_interval):
        activation_time = time.time()
        activation_recheck()
        print("licence still active")
