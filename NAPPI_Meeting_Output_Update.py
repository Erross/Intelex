from requests import get, post, patch
import urllib
import json
### This whole thing is a sequential set of calls to move a complaint along and close it for being non supply chain for NAPPI workflow - it needs to be functionified and made pretty)
#Credentials
username ='$(GIMSUSERNAME)'
password ='$(GIMSPASSWORD)'
GIMSENVIRONMENT = '$(GIMSENVIRONMENT)'
#Record Details and GIMS object
recordNumber = urllib.parse.quote('$(recordnumber)')
objectname ='MonCusComplaint_CustomComplaintObject'
MyAuth = (username, password)

###FUNCTION TO CHANGE ANYTHING @ODATA LINK DEPENDENT

def ILXChange(referenceObject, referencePropertyName, referencePropertyValue, objectName, systemName):
    try:
        objectname = referenceObject
        url = GIMSENVIRONMENT+'api/v2/object/' + objectname +'?$filter='+referencePropertyName+' eq '+"'"+referencePropertyValue+"'"
        response = get(url, auth=MyAuth)
        x = (response.json())
        y = x['value']
        for a in y:
            if a[referencePropertyName] == referencePropertyValue:
                odataLink = a['@odata.editLink']
    except:
        print('failed to get object link for ' + referencePropertyName + " " + referencePropertyValue)
        return('Failed to get object link for'  + referencePropertyName + " " + referencePropertyValue)

    try:
        objectname = objectName
        url = GIMSENVIRONMENT + 'api/v2/object/' + objectname + '(' + objId + ')'
        Body = {}
        bodyName = systemName + "@odata.bind"
        Body[bodyName] = odataLink
        Body = json.dumps(Body)
        myHeaders = {}  # initiate headers
        myHeaders['content-type'] = 'application/json'  # build headers
        params = {'Description': 'string'}  # build params

        response = patch(url, Body, params=params, headers=myHeaders, auth=MyAuth)
        return(response)
    except:
        return ('Failed to change ' + objectname)


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
        return('Failed to change '+ objectname)

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

#CODE TO PUT INTO PILOT onProcess()
context= pilotpython.Context(ctxt)
data= pilotpython.DataRecord(dr)
props = data.getProperties()


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
    props.defineStringProperty('Investigation_Status','Saved and Started')
except:
    print('failed to save and instigate investigation')


#VALIDITY
if len('$(Validity')>0:
    ILXChange('MonCusComplaint_MonValidityObject', 'Caption', '$(Validity)', 'MonCusComplaint_CustomComplaintObject', 'Validity')
    props.defineStringProperty('Validity', '$(Validity)')


if len('$(FunctionKey')>0:
    ILXChange('SyConfiguration_MonsantFunctionObject', 'ImportKey', '$(FunctionKey)', 'MonCusComplaint_CustomComplaintObject', 'Function')
    props.defineStringProperty('FunctionKey', '$(FunctionKey)')
#Change Process
if len('$(ProcessKey)')>0:
    ILXChange('SyConfiguration_MonsantoProcessObject', 'ImportKey', '$(ProcessKey)', 'MonCusComplaint_CustomComplaintObject', 'Process') #verified in test
    props.defineStringProperty('ProcessKey', '$(ProcessKey)')

if len('$(ComplaintCategory)')>0:
    ILXChange('MonCusComplaint_ComplaiCategoryObject', 'Value', '$(ComplaintCategory)', 'MonCusComplaint_CustomComplaintObject', 'ComplaiCategory') #verified in test - must be the code ie PERF_ENV
    props.defineStringProperty('ComplaintCategory', '$(ComplaintCategory)')

if len('$(CSS1)')>0:
    ILXChange('MonCusComplaint_MonCatSubCat1Object', 'SuCategory1Code', '$(CSS1)', 'MonCusComplaint_CustomComplaintObject', 'ComSubCategory1') #verified in test - not code but full thing (may need to change above to match...)
    props.defineStringProperty('CSS1', '$(CSS1)')

if len('$(CSS2)')>0:
    ILXChange('MonCusComplaint_MonCompSubCat12Object', 'SuCategory2Code', '$(CSS2)', 'MonCusComplaint_CustomComplaintObject', 'ComSubCategory2') #verified in test
    props.defineStringProperty('CSS2', '$(CSS2)')

if len('$(ResponsibleSite')>0:
    ILXChange('SysLocationEntity', 'LocationCode', '$(ResponsibleSite)', 'MonCusComplaint_CustomComplaintObject', 'ResponsibleSite') #verified in test
    props.defineStringProperty('Responsible Site', '$(ResponsibleSite)')



if len('$(CCL)') >0:
    ILXChange('SysLocationEntity', 'LocationCode', '$(CCL)', 'MonCusComplaint_CustomComplaintObject', 'CoordinLocation') #verified in test
    props.defineStringProperty('CCL', '$(CCL)')
#change country
if len('$(Country')>0:
    ILXChange('MonAudit_MonsantoCountryObject', 'Caption', '$(Country)', 'MonCusComplaint_CustomComplaintObject', 'CCCountry')
    props.defineStringProperty('Country', '$(Country)')
#change Response to initiator
#THIS ONE CANT USE ILXCHANGE AS IT IS A DIRECT EDIT AND NOT THE ODATA DEPENDENT

if len('$(ResponseToInitiatedBy')>0:
    ILXDirectChange('MonCusComplaint_CustomComplaintObject','RetoInitiatedBy','$(ResponseToInitiatedBy)') #verified in test
    props.defineStringProperty('Response to Initiated By', '$(ResponseToInitiatedBy)')

#change Investigation Detals

if len('$(InvestigationDetails')>0:
    ILXDirectChange('MonCusComplaint_CustomComplaintObject','InvestigDetails','$(InvestigationDetails)') #verified in test
    props.defineStringProperty('InvestigationDetails', '$(InvestigationDetails)')
#CREATE A CAR??!

if len('$(CreateaCAR')>0:
    ILXDirectChange('MonCusComplaint_CustomComplaintObject', 'CreateaCAR', '$(CreateCAR)') #verified in testneed to add a workflow here that automates CAR creation if createacar = TRUE (different script most likely)
    props.defineStringProperty('CreateACAR', '$(CreataCAR)')

#Close Request ONLY DO THIS IF CLOSE = TRUE
#Get workflow id

if '$(CloseComplaint)' == 'TRUE':
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
        props.defineStringProperty('InvestigationClosed', '$(CloseComplaint)')
    except:
        print('failed to close investigation')
        props.defineStringProperty('InvestigationClosed', 'failed to close investigation')