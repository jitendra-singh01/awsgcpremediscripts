import boto3
from datetime import datetime,timezone
client = boto3.client('iam')
users = client.list_users()
user_list = []
now  = datetime.now(timezone.utc)   
more2key = []
for key in users['Users']:
    key_age_expire = False
    result = {}
    Policies = []
    Groups=[]
    result['userName']=key['UserName']
 
    ########################## Check keys #############################
    response = client.list_access_keys(UserName=result["userName"])
    keymetadata = response['AccessKeyMetadata']
    if len(keymetadata)>1:
        more2key.append(result['userName'] + " has 2 keys. Please remove one.")

    ########################### User access key limit###############################
print("##################### User access key limit #####################")
if len(more2key)>0:
    for i in more2key:
        print(i)
else:
    print("Great !!! All IAM users has 1 access key.")