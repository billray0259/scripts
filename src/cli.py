import sys
import openai
import os
import pyperclip

API_KEY_FILE = os.path.expanduser("~/scripts/OPENAI_API_KEY.txt")

def translate_to_terminal_command(text):
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE) as f:
            openai.api_key = f.read().strip()
    elif "OPENAI_API_KEY" in os.environ:
        openai.api_key = os.environ["OPENAI_API_KEY"]
    else:
        print("Please set your OpenAI API key in the OPENAI_API_KEY environment variable or in the OPENAI_API_KEY.txt file.")
        sys.exit(1)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate English text to terminal commands. Respond with only the terminal command and no other text."},
                {"role": "user", "content": text},
            ]
        )
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)
    
    return response.choices[0].message.content


def process_command(command):
    command = command.strip()
    if command.startswith("```") and command.endswith("```"):
        command = command[3:-3].strip()
    if command.startswith("`") and command.endswith("`"):
        command = command[1:-1].strip()
    return command

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cmd.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    translated_command = translate_to_terminal_command(input_string).strip()
    translated_command = process_command(translated_command)
    print(translated_command)
    pyperclip.copy(translated_command)
