import boto3
from datetime import datetime,timezone
client = boto3.client('iam')
users = client.list_users()
policy_vul = []
now  = datetime.now(timezone.utc)   
for key in users['Users']:
    List_of_Policies =  client.list_user_policies(UserName=key['UserName'])
    ########################## Check policy #############################
    if len(List_of_Policies['PolicyNames'])>1:
        policy_vul.append(key['UserName'] + " has user level policy. Please assign group wise policy")

    ########################### User access key limit###############################
print("##################### User level policy vulne #####################")
if len(policy_vul)>0:
    for i in policy_vul:
        print(i)
else:
    print("Great !!! All IAM users does not have user level policy.")