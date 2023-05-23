import boto3
iam = boto3.client('iam')

# List all IAM groups
response = iam.list_groups()
for group in response['Groups']:
    print(group['GroupName'])

# List all groups a user belongs to
response = iam.list_groups_for_user(UserName='USERNAME_HERE')
for group in response['Groups']:
    print(group['GroupName'])
