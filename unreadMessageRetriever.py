import base64
import os

from googleapiclient.discovery import build

import folderGenerator
from authenticator import get_credentials

# Set your API key as an environment variable

creds = get_credentials()


def get_unread_messages_ids(service, label_id):

    try:
        results = service.users().messages().list(userId='me', labelIds=[label_id], q='is:unread').execute()
        messages = results.get('messages', [])

        if not messages:
            print('No unread messages found.')
            return []

        unread_message_ids = [message['id'] for message in messages]
        return unread_message_ids

    except Exception as e:
        print(f'An error occurred while retrieving unread messages: {e}')
        return []


# Mark messages as read
def mark_messages_as_read(service, message_id):
    try:
        service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
        print(f'Marked message {message_id} as read.')

    except Exception as e:
        print(f'An error occurred while marking messages as read: {e}')


# Retrieve email details (subject, sender, body)
def retrieve_email_details(service, email_id):
    try:
        message = service.users().messages().get(userId='me', id=email_id, format='full').execute()
        payload = message['payload']
        headers = payload['headers']
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        sender = next(header['value'] for header in headers if header['name'] == 'From')
        body_data = ''

        parts = payload.get('parts', [])
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body_data = data
                    break

        if body_data:
            # Decode email body
            email_body = base64.urlsafe_b64decode(body_data).decode('utf-8')
        else:
            email_body = ''

        # Retrieve thread ID
        thread_id = message['threadId']

        return subject, sender, email_body, thread_id

    except Exception as e:
        print(f'An error occurred while retrieving email details: {e}')
        return '', '', ''
