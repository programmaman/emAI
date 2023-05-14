from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from authenticator import get_credentials


def get_labels(service):
    """
    Retrieves all labels in a user's Gmail account using the Gmail API.
    :return: A list of label names.
    """
    labels = []

    try:
        # Retrieve a list of labels
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        print(labels)
        return labels

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred retrieving the user\'s labels: {error}')


def get_label_id(service):

    labels = get_labels(service)
    print("Labels Retrieved!")

    # Check if the emAI label exists
    for label in labels:
        if label['name'] == "emAI":
            return label['id']

    # If this code is running, label doesn't exist, so create it and return the id
    new_label = {'name': 'emAI', 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show', 'type': 'user'}

    try:
        created_label = service.users().labels().create(userId='me', body=new_label).execute()
        print("Label created!")
        return created_label['id']

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred creating the emAI label: {error}')
