# First, install the google-colab package

from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Authenticate with Google Cloud Platform using a service account key
# auth.authenticate_user()
# project_id = '1RvccXg4CyXrbyRF9oYr7aaf3YqUpYtzg'
project_id = 'bauddha-patro'
service_account_key = 'bauddha-patro-318cc519bdb4.json'

# Create a credentials object
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

creds = service_account.Credentials.from_service_account_file(service_account_key)


# Create a Google Colab API client
colab = build('notebooks', 'v1', credentials=creds)
# colab_notebooks = colab.notebooks()

# Set the notebook name
notebook_name = 'My Colab Notebook'
command='ls'
# Get the session name for the notebook
response = colab.projects().locations().instances().list(parent=f"projects/{project_id}/locations/-").execute()
instance_name = None
print(response)
for instance in response.get('instances', []):
    if instance['metadata']['runtimeName'] == 'notebook':
        if instance['metadata']['labels'].get('name') == notebook_name:
            instance_name = instance['name']
            break
if not instance_name:
    print(f'Notebook "{notebook_name}" not found')
    exit()

# Start a new session in the notebook
session = colab.projects().locations().instances().sessions().create(parent=instance_name, instance=instance_name).execute()
session_name = session['name']

# Execute the command in the session and print the output
try:
    request = colab.projects().locations().instances().sessions().execute(
        name=session_name,
        requestBody={
            'code': command,
            'outputs': [{'notebookOutput': {'dataType': 'STRING'}}]
        }
    )
    response = request.execute()
    output = response['outputs'][0]['notebookOutput']['data']
    print(output)
except HttpError as error:
    print(f'An error occurred: {error}')

# Delete the session
colab.projects().locations().instances().sessions().delete(name=session_name).execute()
