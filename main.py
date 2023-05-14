import time
from plyer import notification
import authenticator
import chatGpt
import folderGenerator
from googleapiclient.discovery import build

import messageSender
from unreadMessageRetriever import get_unread_messages_ids, retrieve_email_details, mark_messages_as_read


def process_emails():
    # Fetch unread messages
    unread_message_ids = get_unread_messages_ids(service, label_id)

    if unread_message_ids:
        for message_id in unread_message_ids:
            subject, sender, email_body, thread_id = retrieve_email_details(service, message_id)
            print(f"Subject: {subject}")
            print(f"Sender: {sender}")
            print(f"Email Body:\n{email_body}")

            if email_body:
                prompt = f"Subject: {subject}\nSender: {sender}\n\n{email_body}"
                print("Prompt:", prompt)
                response = chatGpt.send_to_chatgpt(prompt)
                # Print the response
                print(f'GPT Response:\n{response}')
                mark_messages_as_read(service, message_id)

                # Ask for user confirmation
                confirm = get_user_confirmation(sender, subject, response)

                if confirm is True:
                    messageSender.send_reply_email(service, sender, "Re: " + subject, response, thread_id)
                elif isinstance(confirm, str):
                    messageSender.send_reply_email(service, sender, "Re: " + subject, confirm, thread_id)
                else:
                    print("Response not sent. User declined confirmation.")


def get_user_confirmation(sender, subject, response):
    print("Automated Response:")
    print(f"Subject: {subject}")
    print(f"Sender: {sender}")
    print(f"Response:\n{response}")

    # Configure the notification
    notification_title = "Automated Response"
    notification_message = f"Subject: {subject}\nSender: {sender}\n\n{response}"

    # Display the desktop notification
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_icon=None,  # Path to the app icon if you have one
        timeout=10  # Time in seconds the notification should stay visible
    )

    while True:
        user_input = input("Send the above response? (y/n/e): ")
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        elif user_input.lower() == 'e':
            edited_response = input("Enter the edited response: ")
            return edited_response
        else:
            print("Invalid input. Please enter 'y' for Yes, 'n' for No, or 'e' to edit the response.")



if __name__ == '__main__':
    # Initialize and authenticate APIs
    creds = authenticator.get_credentials()
    chatGpt.create_openai_api()

    # Build Service
    service = build('gmail', 'v1', credentials=creds)

    # Specify the label ID (replace with your desired label ID)
    label_id = folderGenerator.get_label_id(service)

    while True:
        process_emails()

        # Delay for a certain amount of time before checking for new emails again
        time.sleep(300)  # Sleep for 60 seconds (adjust as needed)
