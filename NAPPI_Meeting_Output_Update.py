from requests import get
from requests import post
import urllib
import json
from requests import patch
### This whole thing is a sequential set of calls to move a complaint along and close it for being non supply chain for NAPPI workflow - it needs to be functionified and made pretty)
#Credentials
username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
GIMSENVIRONMENT = $(GIMSENVIRONMENT)'
#Record Details and GIMS object
recordNumber = urllib.parse.quote('$(recordnumber)')
objectname ='MonCusComplaint_CustomComplaintObject'
MyAuth = (username, password)

###FUNCTION TO CHANGE ANYTHING @ODATA LINK DEPENDENT

def ILXChange(referenceObject, referencePropertyName, referencePropertyValue, objectName, systemName):
    try:
        objectname = referenceObject
        url = GIMSENVIRONMENT+'api/v2/object/' + objectname
        response = get(url, auth=MyAuth)
        x = (response.json())
        y = x['value']
        for a in y:
            if a[referencePropertyName] == referencePropertyValue:
                odataLink = a['@odata.editLink']
    except:
        print('failed to get object link for ' + referencePropertyName + " " + referencePropertyValue)

    #Change Validity

    try:
        objectname = objectName
        url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')'
        Body = {}
        bodyName = systemName+"@odata.bind"
        Body[bodyName] = odataLink
        Body = json.dumps(Body)
        myHeaders = {} #initiate headers
        myHeaders['content-type'] = 'application/json' #build headers
        params = {'Description': 'string'} #build params

        response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
    except:
        print('failed to change ' + objectName)
        return('Failed to change '+ objectname)

def ILXDirectChange(objectName,systemName,stringInput):
    try:
        objectname = objectName
        url = GIMSENVIRONMENT+'api/v2/object/'+objectname+'('+objId+')'
        Body = {}
        bodyName = systemName
        Body[bodyName] = stringInput
        Body = json.dumps(Body)
        myHeaders = {} #initiate headers
        myHeaders['content-type'] = 'application/json' #build headers
        params = {'Description': 'string'} #build params

        response = patch(url, Body, params = params,headers=myHeaders, auth=MyAuth)
    except:
        print('failed to change ' + objectName)
        return('Failed to change '+ objectname)

###This whole thing needs to write
#Validity
#Investigation Details
#Function
#Process
#Complaintcategory
#ComplaintSub1
#ComplaintSub2
#Country
#ResponsibleSite
#Complaint coordinator location
#Create CAR? (may need whole workflow for this...
#Close Complaint
#Response to Init
#get object ID for the RECORD

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
#Get available action status for save and Submit Complaint - SETS RECORD UP FOR USE AND MAKES CLOSING AN OPTION IF NEED BE
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
#VALIDITY
ILXChange('MonCusComplaint_MonValidityObject', 'Caption', '$(Validity)', 'MonCusComplaint_CustomComplaintObject', 'Validity@odata.bind')
#ILXChange(referenceObject, referencePropertyName, referencePropertyValue, objectName, systemName)
ILXChange('MonCusComplaint_MonFunctionObject', 'ImportKey', '$(FunctionKey)', 'MonCusComplaint_CustomComplaintObject', 'Function@odata.bind')
#Change Process
ILXChange('SyConfiguration_MonsantoProcessObject', 'ImportKey', '$(ProcessKey)', 'MonCusComplaint_CustomComplaintObject', 'Process@odata.bind')
#Change Complaint Category
ILXChange('MonCusComplaint_ComplaiCategoryObject', 'Value', '$(ComplaintCategory)', 'MonCusComplaint_CustomComplaintObject', 'ComplaiCategory@odata.bind')
#Change CS1
ILXChange('MonCusComplaint_MonCatSubCat1Object', 'ComSubCategory1', '$(CSS1)', 'MonCusComplaint_CustomComplaintObject', 'ComSubCategory1@odata.bind')
#Change CS2
ILXChange('MonCusComplaint_MonCompSubCat12Object', 'ComSubCategory2', '$(CSS2)', 'MonCusComplaint_CustomComplaintObject', 'ComSubCategory2@odata.bind')
#Change Country
#NEED TO ADD COUNTRYT TO LIST - DONT HAVE!!
#Change Responsible Site
ILXChange('SysLocationEntity', 'LocationCode', '$(Responsible Site)', 'MonCusComplaint_CustomComplaintObject', 'ResponsibleSite@odata.bind')
#change CCL
ILXChange('SysLocationEntity', 'LocationCode', '$(CCL)', 'MonCusComplaint_CustomComplaintObject', 'CoordinLocation@odata.bind')

#change Response to initiator
#THIS ONE CANT USE ILXCHANGE AS IT IS A DIRECT EDIT AND NOT THE ODATA DEPENDENT

ILXDirectChange('MonCusComplaint_CustomComplaintObject',RetoInitiatedBy,'$(ResponseToInitiatedBy)')

#change Investigation Detals

ILXDirectChange('MonCusComplaint_CustomComplaintObject',InvestigDetails,'$(InvestigationDetails)')



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