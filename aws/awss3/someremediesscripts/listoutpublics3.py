import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler():
    s3 = boto3.client('s3') 
    s3res = boto3.resource('s3')
    for bucket in s3res.buckets.all():  
        try:   
            policy = s3.get_bucket_policy_status(Bucket=bucket.name)
            if policy["PolicyStatus"]["IsPublic"] == True:
                print("{} Bucket is public.".format(bucket.name)) 
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
               print("{} Bucket is not encrypted.".format(bucket.name)) 

lambda_handler()