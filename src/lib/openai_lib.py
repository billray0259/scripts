import dotenv
dotenv.load_dotenv()

import openai

class ApiKeyError(Exception):
    pass


def chat_prompt(system_message, user_messages, model="gpt-3.5-turbo"):
    if type(user_messages) == str:
        user_messages = [user_messages]
    user_messages = [{"role": "user", "content": message} for message in user_messages]

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message}] + user_messages
    )

    return response.choices[0].message.content