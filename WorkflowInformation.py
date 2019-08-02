from requests import get
from requests import patch
import urllib
import json
from requests import post

username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
recordNumber = urllib.parse.quote('60907')
objectname ='MonCusComplaint_CustomComplaintObject'


MyAuth = (username, password)
url = 'https://clients.intelex.com/Login3/Monsanto/api/v2/object/' + objectname + "?$filter=RecordNumber eq "+recordNumber
response = get(url, auth=MyAuth)
x = (response.json())

y = x.get('value')
z = y[0]

fullid = z['@odata.id'] #get the start of the value (needs more parsing)
fullid_split = fullid.split("(") #Split string part the first
objId = fullid_split[1].split(")")[0] #split string part the second

url = 'https://clients.intelex.com/Login3/Monsanto/api/v2/object/'+objectname+'('+objId+')/Workflow/CurrentStage/Actions' #returns currently available actions on a record

response = get(url, auth=MyAuth)
x = response.json()
y = x['value']
print(type(y))
for a in y:
    print(a)