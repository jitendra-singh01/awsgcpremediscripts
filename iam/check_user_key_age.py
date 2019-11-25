import boto3
from datetime import datetime,timezone
client = boto3.client('iam')
users = client.list_users()
user_list = []
mfalist = []
keyagevul = []
KEY_AGE_DAYS = 90
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

    for key in keymetadata:
        duration = now - key['CreateDate']   
        duration = duration.days
        if duration >= KEY_AGE_DAYS:
            keyagevul.append(result['userName'] + "'s key age expired. It is time to create new.")
            break

print("################### User access key age vulnerability #################")
if len(keyagevul)>0:
    for i in keyagevul:
        print(i)
else:
    print("Great !!! All IAM users access key is in active life cycle.")
# for key in user_list:
#     print(key)