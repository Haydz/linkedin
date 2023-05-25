import boto3

iam = boto3.client('iam')
response = iam.get_group(GroupName='Admin')

group = response['Group']
print(f"GroupName: {group['GroupName']}")
print(f"GroupId: {group['GroupId']}")
print(f"Arn: {group['Arn']}")
print(f"CreateDate: {group['CreateDate']}")
print(f"Path: {group['Path']}")

#or print like this:
group_all = f"Group: {group['GroupName']} | {group['GroupId']} | {group['CreateDate']}"
print(group_all)