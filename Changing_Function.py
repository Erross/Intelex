from requests import get
from requests import patch
import urllib
import json
from requests import post

username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
GIMSENVIRONMENT = 'https://clients.intelex.com/Login3/Monsanto/'''#enter your environment prod/test etc
recordNumber = urllib.parse.quote('2')
objectname ='MonCusComplaint_CustomComplaintObject'


MyAuth = (username, password)
url = GIMSENVIRONMENT'api/v2/object/' + objectname + "?$filter=RecordNumber eq " + recordNumber
response = get(url, auth=MyAuth)
x = (response.json())

y = x.get('value')
z = y[0]

fullid = z['@odata.id'] #get the start of the value (needs more parsing)
fullid_split = fullid.split("(") #Split string part the first
objId = fullid_split[1].split(")")[0] #split string part the second

url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')'
Body = {}
Body['Function@odata.bind'] = GIMSENVIRONMENT+'api/v2/object/SyConfiguration_MonsantFunctionObject(c7eded55-286f-4879-91b8-16d410eaca70)' #here you need to put in a specific function's ID - this one corresponds to some function or other
Body = json.dumps(Body)
myHeaders = {} #initiate headers
myHeaders['content-type'] = 'application/json' #build headers
params = {'Description': 'string'} #build params

response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
print(response)
print(response.json())
print(response.content)