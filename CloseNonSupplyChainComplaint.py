from requests import get
from requests import post
import urllib
import json
from requests import patch
### This whole thing is a sequential set of calls to move a complaint along and close it for being non supply chain for NAPPI workflow - it needs to be functionified and made pretty)
#Credentials
GIMSENVIRONMENT = '$(GIMSENVIRONMENT)'
username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
#Record Details and GIMS object
recordNumber = urllib.parse.quote('$(recordnumber)')
objectname ='MonCusComplaint_CustomComplaintObject'
MyAuth = (username, password)
functionKey = 'ResearchSupply ChainRow Crop'
processKey = 'ResearchBreedingSupply ChainRow Crop'

#get object ID
try:
    url = GIMSENVIRONMENT+'api/v2/object/' + objectname + "?$filter=RecordNumber eq "+ recordNumber
    response = get(url, auth=MyAuth)
    x = (response.json())

    y = x.get('value')
    z = y[0]

    fullid = z['@odata.id'] #get the start of the value (needs more parsing)
    fullid_split = fullid.split("(") #Split string part the first
    objId = fullid_split[1].split(")")[0] #split string part the second
except:
    print('failed to get an objectid')

#Get available action status for save and Submit Complaint
try:
    url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')/Workflow/CurrentStage/Actions'
    response = get(url, auth=MyAuth)
    x = response.json()

    for y in x['value']:
        if y['Name'] == 'Save and Submit Complaint':
            odataID = y['Id']

except:
    print('failed to get odataID')

#Save and Submit complaint

try:
    url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')/Workflow/CurrentStage/Actions('+odataID+')/Action.ExecuteStageAction'

    response = post(url, auth=MyAuth)
except:
    print('failed to save and instigate investigation')

#Find Validity Value

try:
    objectname ='MonCusComplaint_MonValidityObject'
    url = GIMSENVIRONMENT+'api/v2/object/' + objectname
    response = get(url, auth=MyAuth)
    x = (response.json())
    y = x['value']
    for a in y:
        if a['Caption'] == 'Non Supply Chain':
            odataLink = a['@odata.editLink']
except:
    print('failed to get validity object link')





#Change Validity

try:
    objectname = 'MonCusComplaint_CustomComplaintObject'

    url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')'
    Body = {}
    Body['Validity@odata.bind'] = odataLink
    Body = json.dumps(Body)
    myHeaders = {} #initiate headers
    myHeaders['content-type'] = 'application/json' #build headers
    params = {'Description': 'string'} #build params

    response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
except:
    print('failed to change validity')

#Change Function
#1 Get function odatalink

try:
    objectname ='SyConfiguration_MonsantFunctionObject'
    url = GIMSENVIRONMENT+'api/v2/object/' + objectname
    response = get(url, auth=MyAuth)
    x = (response.json())
    y = x['value']
    for a in y:
        if a['ImportKey'] == functionKey: #this needs to be the Function Key Value
            fxnodataLink = a['@odata.editLink']
            print("fxnlnk "+ fxnodataLink)
except:
    print('failed to get function ODATA link')
#2 Change function
try:
    objectname = 'MonCusComplaint_CustomComplaintObject'

    url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')'
    Body = {}
    Body['Function@odata.bind'] = fxnodataLink
    Body = json.dumps(Body)
    myHeaders = {} #initiate headers
    myHeaders['content-type'] = 'application/json' #build headers
    params = {'Description': 'string'} #build params

    response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
except:
    print('failed to change function')

#Change Process
#1 Get process odatalink
try:
    objectname ='SyConfiguration_MonsantoProcessObject'
    print('a')
    url = GIMSENVIRONMENT+'api/v2/object/' + objectname + "?$filter=ImportKey eq '" +processKey +"'" #this too needs to be the thing
    print('a')
    response = get(url, auth=MyAuth)
    print('a')
    x = (response.json())
    print(x)
    print('a')
    y = x['value']
    print('a')
    for a in y:
        if a['ImportKey'] == processKey: #this needs to be the Process Key Value
            prcodataLink = a['@odata.editLink']
            print("prclnk "+ prcodataLink)
except:
    print('failed to get process ODATA link')
#2 Change process
try:
    objectname = 'MonCusComplaint_CustomComplaintObject'

    url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')'
    Body = {}
    Body['Process@odata.bind'] = prcodataLink
    Body = json.dumps(Body)
    print(odataLink)
    myHeaders = {} #initiate headers
    myHeaders['content-type'] = 'application/json' #build headers
    params = {'Description': 'string'} #build params

    response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
    print(response)
    print(response.content)
except:
    print('failed to change process')





#Close Request
#Get workflow id


try:
    url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')/Workflow/CurrentStage/Actions'
    response = get(url, auth=MyAuth)
    x = response.json()

    for y in x['value']:
        if y['Name'] == 'Complete Complaint':
            odataID2 = y['Id']


    print("odataID2 "+odataID2)
except:
    print('failed to get odataID2')

try:
    url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')/Workflow/CurrentStage/Actions('+odataID2+')/Action.ExecuteStageAction'

    response = post(url, auth=MyAuth)
except:
    print('failed to close investigation')