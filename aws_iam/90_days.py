import boto3


from datetime import datetime, timedelta, timezone

# Define the date 90 days ago from now, as a timezone-aware datetime object
ninety_days_ago = datetime.now(timezone.utc) - timedelta(days=90)
# Use the default session
iam_client = boto3.client('iam')
# Get a paginator to list all users
paginator = iam_client.get_paginator('list_users')
# Initialize a list to store the users who haven't used their password for 90 days
inactive_users = []

# Use the paginator to go through each page of users
for page in paginator.paginate():
    for user in page['Users']:
        # Some users might not have a 'PasswordLastUsed' key, so we use the dict.get() method which won't raise an error if the key is not present
        password_last_used = user.get('PasswordLastUsed')
        # If the user has never used their password or last used it more than 90 days ago, we add them to our list
        if password_last_used is None or password_last_used < ninety_days_ago:
            inactive_users.append(user['UserName'])
        else:
            print("recent user:", user['UserName'])

# Print the inactive users
print("Users who haven't used their password in the last 90 days:")
for user in inactive_users:
    print(user)
