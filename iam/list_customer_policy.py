import boto3
from datetime import datetime,timezone
import re
client = boto3.client('iam')
i = 1;
policy_resource_vul = []
policy_action_vul = []
policy_not_vul = []
action_vul_str = "Policy {} is performing all actions. Please specify needed actions."
resource_vul_str = "Policy {} is providing permission tp all resources. Please specify needed resources."
not_vul_str = "Policy {}, has healthy policy statement."
process_policies = 10
max_item = 10
def list_out_iam_policy(next=""):
	global i,max_item
	count = 1;
	if next != "":
		policies = client.list_policies(Scope='Local',Marker=next,MaxItems=max_item)
	else:
		policies = client.list_policies(Scope='Local',MaxItems=max_item)
	istruncate = policies['IsTruncated']
	tpolicies = policies['Policies']
	for p in tpolicies:
		get_policy_response = client.get_policy(PolicyArn=p['Arn'])
		version_id = get_policy_response['Policy']['DefaultVersionId']

		# Get default version of policy
		get_policy_version_response = client.get_policy_version(
		    PolicyArn=p['Arn'],	
		    VersionId=version_id,
		)

		policy_document = get_policy_version_response['PolicyVersion']['Document']
		
		statements = policy_document['Statement']
		#@print(policy_document['Statement'])
		for statement in statements:
			resource = None
			action = None
			has_action = 0
			has_resource = 0
			if isinstance(statement,dict):
				if 'Resource' in statement:
					resource = str(statement['Resource'])
				if "Action" in statement:
					action = str(statement['Action'])
				
				if action is not None and re.match(r"[*]",action): 
					has_action = has_action + 1

				if resource is not None and re.match(r"[*]",resource):
					has_resource = has_resource + 1

		if has_resource>0:
			policy_resource_vul.append(resource_vul_str.format(p['PolicyName']))

		if has_action>0:
			policy_action_vul.append(action_vul_str.format(p['PolicyName']))
			
		if has_action == 0 and has_resource == 0:
			policy_not_vul.append(not_vul_str.format(p['PolicyName']))

		i = i+1
		count = count + 1
		if i%10 == 0:
			print("Processed "+str(i) + " policies")
		if count == len(policies):
			if istruncate == True:
				list_out_iam_policy(policies['Marker'])

	
list_out_iam_policy()
print("Processed "+str(i) + " policies")
print("Showing calculated result ....")
if(len(policy_action_vul) > 0):
	print("############## Need to specify actions by action name "+str(len(policy_action_vul))+" out of "+len(i-1)+"###########.")
	for p in policy_action_vul:
		print(p)

if(len(policy_resource_vul) > 0):
	print("############## Need to specify resource by name to "+str(len(policy_resource_vul))+" out of "+len(i-1)+"###########")
	for p in policy_resource_vul:
		print(p)

if(len(policy_not_vul) > 0):
	print("############## "+str(len(policy_not_vul))+" Policies are good out of "+str(i-1)+"###########")
	for p in policy_not_vul:
		print(p)