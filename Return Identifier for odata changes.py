from requests import get
import urllib
GIMSENVIRONMENT = $(GIMSENVIRONMENT)'
username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
recordNumber = urllib.parse.quote('2')
objectname ='SyConfiguration_MonsantoProcessObject' #System name - hit different objects for different responses, each will have unique filters etc

print(recordNumber)


MyAuth = (username, password)


#part 1 - Obtain object ID for the complaint object
url = GIMSENVIRONMENT+'api/v2/object/' + objectname + "?$filter=ImportKey eq"+" 'AdministrativeManufacturing OperationsSupply ChainRow Crop'" #this works for this object, not others
response = get(url, auth=MyAuth)
x = (response.json())
y = x['value']
for a in y:
    print(a['ImportKey']) #NOT ALWAYS IMPORT KEY!!