import os

import openai


# Set up OpenAI API
def create_openai_api():
    try:
        with open('api_key.txt', 'r') as file:
            api_key = file.read().strip()
    except FileNotFoundError:
        api_key = input("API key file not found. Please enter your API key: ")
        with open('api_key.txt', 'w') as file:
            file.write(api_key)
    openai.api_key = api_key


def send_to_chatgpt(message_content):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt="Respond to the message below as if you are the recipient. \n" + message_content,
        max_tokens=3500,
        temperature=0.7
    )
    return response.choices[0].text.strip()
