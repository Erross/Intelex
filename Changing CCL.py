from requests import get
from requests import patch
import urllib
import json
from requests import post

username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
recordNumber = urllib.parse.quote('')
objectname ='MonCusComplaint_CustomComplaintObject'

MyAuth = (username, password)
url = 'https://clients.intelex.com/Login3/Monsanto/api/v2/object/' + objectname + "?$filter=RecordNumber eq " + recordNumber
response = get(url, auth=MyAuth)
x = (response.json())

y = x.get('value')
z = y[0]

fullid = z['@odata.id'] #get the start of the value (needs more parsing)
fullid_split = fullid.split("(") #Split string part the first
objId = fullid_split[1].split(")")[0] #split string part the second

print(objId)
url = 'https://clients.intelex.com/Login3/Monsanto/api/v2/object/'+objectname+'('+objId+')'
Body = {}
Body['CoordinLocation@odata.bind'] ='https://clients.intelex.com/Login3/Monsanto/api/v2/object/MonAudit_MonRegionObject('+CCLID_')' #Have to use another fxn to get the CCL (ie return identifier)
Body = json.dumps(Body)
myHeaders = {} #initiate headers
myHeaders['content-type'] = 'application/json' #build headers
params = {'Description': 'string'} #build params

response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
print(response)

