import boto3
import json

iam = boto3.client('iam')

username = 'username'  # replace with your user name

def print_policies(response):
    for policy in response['AttachedPolicies']:
        policy_arn = policy['PolicyArn']

        # Get the policy details
        policy_version = iam.get_policy(PolicyArn=policy_arn)['Policy']['DefaultVersionId']
        policy_document = iam.get_policy_version(PolicyArn=policy_arn, VersionId=policy_version)['PolicyVersion']['Document']

        print(f"Policy Name: {policy['PolicyName']}")
        print(f"Policy Document: {json.dumps(policy_document, indent=4)}\n")


# Get the policies attached to the user
response = iam.list_attached_user_policies(UserName=username)
print(f"Policies for user {username}:")
print_policies(response)

# Get the groups the user is in
response = iam.list_groups_for_user(UserName=username)

for group in response['Groups']:
    print(f"Policies for group {group['GroupName']}:")
    group_response = iam.list_attached_group_policies(GroupName=group['GroupName'])
    print_policies(group_response)
