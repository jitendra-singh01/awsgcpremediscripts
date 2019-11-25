import boto3
from datetime import datetime,timezone
client = boto3.client('iam')
users = client.list_users()
user_list = []
mfalist = [] 
more2key = []
for key in users['Users']:
    key_age_expire = False
    result = {}
    Policies = []
    Groups=[]
    result['userName']=key['UserName']
    has_pass = False
    try:
        login_profile = client.get_login_profile(UserName=result['userName'])
        has_pass = True
    except:
        has_pass = False

    List_of_MFA_Devices = client.list_mfa_devices(UserName=key['UserName'])

    if not len(List_of_MFA_Devices['MFADevices']):
        result['isMFADeviceConfigured']=False   
    else:
        result['isMFADeviceConfigured']=True    
    
    ########################### Check MFA is on or not ###################
    if has_pass == True and result['isMFADeviceConfigured'] == False:
        mfalist.append(result['userName'] + " is on risk. Please enable MFA for this user.")
    else:
        mfalist.append(result['userName'] + " has programmatic access.")

    
########################### MFA Vulnerability###############################
print("######################### MFA Vulnerability #########################")
if len(mfalist)>0:
    for i in mfalist:
        print(i)
else:
    print("Great !!! There is no MFA vulnerability") 
# for key in user_list:
#     print(key)