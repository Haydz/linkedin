import boto3

iam = boto3.client('iam')

# Assume 'username' is the IAM user who has been detected as unused
username = 'boto3'

# Detach policies
for policy in iam.list_attached_user_policies(UserName=username)['AttachedPolicies']:
    iam.detach_user_policy(UserName=username, PolicyArn=policy['PolicyArn'])

# Remove from groups
for group in iam.list_groups_for_user(UserName=username)['Groups']:
    iam.remove_user_from_group(UserName=username, GroupName=group['GroupName'])

# Deactivate access keys
for key_metadata in iam.list_access_keys(UserName=username)['AccessKeyMetadata']:
    if key_metadata['Status'] == 'Active':
        iam.update_access_key(UserName=username, AccessKeyId=key_metadata['AccessKeyId'], Status='Inactive')

# Confirm that access has been removed

# Confirm no policies are attached
if not iam.list_attached_user_policies(UserName=username)['AttachedPolicies']:
    print(f"All policies detached for {username}")

# Confirm no group membership
if not iam.list_groups_for_user(UserName=username)['Groups']:
    print(f"{username} is not a member of any group")

# Confirm no active access keys
if not any(key_metadata['Status'] == 'Active' for key_metadata in iam.list_access_keys(UserName=username)['AccessKeyMetadata']):
    print(f"No active access keys for {username}")
