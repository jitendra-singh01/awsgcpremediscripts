import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler():
    s3 = boto3.client('s3') 
    s3res = boto3.resource('s3')
    for bucket in s3res.buckets.all():
        try:   
            enc = s3.get_bucket_encryption(Bucket=bucket.name)
            rules = enc['ServerSideEncryptionConfiguration']['Rules']
            enctype = rules[0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
            if enctype != "aws:kms" and enctype!="AES256":
                print("{} Bucket is not encrypted.".format(bucket.name))
        except ClientError as e:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
               print("{} Bucket is not encrypted.".format(bucket.name)) 

lambda_handler()