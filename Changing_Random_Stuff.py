from requests import get
from requests import patch
import urllib
import json
from requests import post
GIMSENVIRONMENT = $(GIMSENVIRONMENT)'
username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
recordNumber = urllib.parse.quote('2')
objectname ='MonCusComplaint_CustomComplaintObject' #for different objects this would have to change - requires admin role to see object names in ILX


MyAuth = (username, password)
url = GIMSENVIRONMENT+'api/v2/object/' + objectname + "?$filter=RecordNumber eq "+ recordNumber #filters can change here - admin can see system names of properties
response = get(url, auth=MyAuth)
x = (response.json())

y = x.get('value')
z = y[0]

fullid = z['@odata.id'] #get the start of the value (needs more parsing)
fullid_split = fullid.split("(") #Split string part the first
objId = fullid_split[1].split(")")[0] #split string part the second

url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')'
Body = {}
Body['ComSubCategory1@odata.bind'] =GIMSENVIRONMENT+'api/v2/object/MonCusComplaint_MonCatSubCat1Object(8c69d243-f5db-4151-b811-bf7aad790082)' #example here changes the sub catefory 1 to an object identified through another script
#8c69d243-f5db-4151-b811-bf7aad790082

Body = json.dumps(Body)
myHeaders = {} #initiate headers
myHeaders['content-type'] = 'application/json' #build headers
params = {'Description': 'string'} #build params

response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
print(response)
print(response.content)
