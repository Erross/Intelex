from requests import get
import urllib
GIMSENVIRONMENT = $(GIMSENVIRONMENT)'
username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
recordNumber = urllib.parse.quote('2')
objectname ='MonCusComplaint_CustomComplaintObject' #change if hitting different objects


MyAuth = (username, password)

#part 1 - Obtain object ID for the complaint object
url = GIMSENVIRONMENT+'api/v2/object/' + objectname + "?$filter=RecordNumber eq "+recordNumber
response = get(url, auth=MyAuth)
x = (response.json())

y = x.get('value')
z = y[0]

fullid = z['@odata.id']  # get the start of the value (needs more parsing)
fullid_split = fullid.split("(")  # Split string part the first
objId = fullid_split[1].split(")")[0]  # split string part the second

url = GIMSENVIRONMENT+'api/v2/object/' + objectname + "("+objId+")/ILX.Attachments" #returns attachments details if any exist

response = get(url,auth=MyAuth)
x = (response.json())
print(x['value'])
