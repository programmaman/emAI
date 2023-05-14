import base64

from googleapiclient.errors import HttpError


def send_reply_email(service, sender, subject, message_body, thread_id=None):
    """Sends a reply email using the Gmail API.

    Args:
        service (googleapiclient.discovery.Resource): An authenticated Gmail API service object.
        sender (str): Email address of the sender.
        subject (str): Email subject.
        message_body (str): Email body.
        thread_id (str): ID of the thread to reply to.

    Returns:
        dict: Sent email information.
    """
    message = create_message(sender, subject, message_body, thread_id=thread_id)
    try:
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        return sent_message
    except HttpError as error:
        raise HttpError(f"An error occurred while sending the reply email: {error}")


def create_message(sender, subject, message_body, thread_id=None):
    """Creates a message for sending a reply.

    Args:
        sender (str): Email address of the sender.
        subject (str): Email subject.
        message_body (str): Email body.
        thread_id (str, optional): ID of the thread to reply to. Defaults to None.

    Returns:
        dict: Message object.
    """
    message = {
        'raw': base64.urlsafe_b64encode(
            f"From: {sender}\r\n"
            f"To: {sender}\r\n"
            f"Subject: {subject}\r\n"
            f"In-Reply-To: {thread_id}\r\n"
            f"References: {thread_id}\r\n"
            f"\r\n"
            f"{message_body}"
            .encode()
        ).decode()
    }
    return message
