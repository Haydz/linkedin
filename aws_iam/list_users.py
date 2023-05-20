import boto3
iam = boto3.client('iam')
users = iam.list_users()

for user in users['Users']:
    print(user['UserName'])
   
"""
Example of user object
{'Path': '/', 'UserName': 'remove_perms', 'UserId': 'AIDAQCCYXUUI5XR', 'Arn': 'arn:aws:iam::0044XXXX357:user/remove_perms', 'CreateDate': datetime.datetime(2023, 4, 4, 14, 55, 46, tzinfo=tzutc())}
"""