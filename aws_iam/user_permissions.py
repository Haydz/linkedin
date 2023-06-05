import boto3
import json

iam = boto3.client('iam')

username = 'boto3'  # replace with your user name

# Get the policies attached to the user
response = iam.list_attached_user_policies(UserName=username)

for policy in response['AttachedPolicies']:
    policy_arn = policy['PolicyArn']
    
    # Get the policy details
    policy_version = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
    policy_document = iam.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document']
    
    print(f"Policy Name: {policy['PolicyName']}")
    print(f"Policy Document: {json.dumps(policy_document, indent=4)}\n")
