username = 'gimsfasa1@monsanto.com'
password = 'MonFasa1'
GIMSENVIRONMENT = 'https://preprod-na.intelex.com/Login3/MonsantoTest/'

###gimsfasa1@monsanto.com
##MonFasa1
##gimsfasa2@monsanto.com
##MonFasa2
##gimsfasa3@monsanto.com
##MonFasa3
##gimsfasa4@monsanto.com
##MonFasa4
##gimsfasa5@monsanto.com
##MonFasa5
from requests import get
from requests import patch
import urllib
import json
from requests import post

def ILXGetRef(referenceObject, referencePropertyName, referencePropertyValue, objectName, systemName):
    try:
        objectname = referenceObject
        url = GIMSENVIRONMENT+'/api/v2/object/' + objectname
        response = get(url, auth=MyAuth)
        x = (response.json())
        y = x['value']
        for a in y:
            if a[referencePropertyName] == referencePropertyValue:
                odataLink = a['@odata.editLink']
                return(odataLink)
    except Exception as e:
        print('failed to get object link for ' + referencePropertyName + " " + referencePropertyValue + " ")
        print(e)
        return(e)



recordNumber = urllib.parse.quote('2')
objectname ='MonAudit_MonsantoCARObject'
MyAuth = (username, password)

print('1')
odataLink = ILXGetRef('SysLocationEntity', 'Name', 'Row Crop', 'MonCusComplaint_CustomComplaintObject', 'CoordinLocation@odata.bind')
print(odataLink)
print('2')
print(odataLink)
url = GIMSENVIRONMENT+'/api/v2/object/' + objectname
Body = {}

Body['Location'+"@odata.bind"] = odataLink
Body = json.dumps(Body)
myHeaders = {} #initiate headers
myHeaders['content-type'] = 'application/json' #build headers
params = {'Description': 'string'} #build params


response = post(url, Body, params = params,headers=myHeaders, auth=MyAuth)
print(response.content)