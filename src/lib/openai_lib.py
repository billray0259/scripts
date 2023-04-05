import os
import sys
import openai


class ApiKeyError(Exception):
    pass


def get_api_key(api_key_file="~/scripts/OPENAI_API_KEY.txt"):
    api_key_file = os.path.expanduser(api_key_file)
    if os.path.exists(api_key_file):
        with open(api_key_file) as f:
            return f.read().strip()
    elif "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]
    else:
        raise ApiKeyError("Please set your OpenAI API key in the OPENAI_API_KEY environment variable or in the OPENAI_API_KEY.txt file.")


def chat_prompt(system_message, user_messages, model="gpt-3.5-turbo"):
    if type(user_messages) == str:
        user_messages = [user_messages]
    user_messages = [{"role": "user", "content": message} for message in user_messages]

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message}] + user_messages
    )

    return response.choices[0].message.content