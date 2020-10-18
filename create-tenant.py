import requests
import json
from credentials import *


###
#   Description:    LOGS IN TO APIC USING THE CREDENTIALS OBTAINED FROM "credentials.py"
#   Params:         None
#   Returns:        The response object resulting from the Login API call
###
def login():
    endpoint = "/api/aaaLogin.json"
    url = "https://{}:{}{}".format(hostname, port, endpoint)
    creds = {
        "aaaUser": {"attributes": {"name": username, "pwd": password}}
    }
    return requests.post(url, data=json.dumps(creds), verify=False)


###
#   Description:    CREATES A TENANT
#   Params:         Expects Tenant name and cookies (obtained from login) to be supplied as parameters
#   Returns:        The response object resulting from the Create tenant API call
###
def createTenant(tnt_name, apic_cookies):
    endpoint = "/api/mo/uni/{}.json".format(tnt_name)
    url = "https://{}{}".format(hostname, endpoint)
    req_body = {
        "fvTenant": {
            "attributes": {
                "descr": "The Support Organization Tenant",
                "dn": "uni/{}".format(tnt_name),
                "name": "Test",
                "rn": tnt_name,
                "status": "created,modified"
            }
        }
    }
    return requests.post(url, data=json.dumps(req_body), cookies=apic_cookies, verify=False)


##################
#   MAIN FUNCTION
##################
def main():
    tenant_name = "tn-Test"         ## Declaring Tenant Name

    login_response = login()        ## Calling the Login function
    print("LOGIN RESPONSE")
    print(login_response.text)      ## Printing the Login Response Body


    apic_cookies = login_response.cookies       ## Parsing the cookies from Login response
    create_tn_response = createTenant(tenant_name, apic_cookies)        ## Calling the Create Tenant function
    print("\nCREATE TENANT RESPONSE")
    print(create_tn_response.text)      ## Printing the Create Tenant Response Body

if __name__ == "__main__":
    main()