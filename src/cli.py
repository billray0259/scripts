import sys
import pyperclip

import lib.openai_lib as openai_lib
import openai





def translate_to_terminal_command(text):
    try:
        return openai_lib.chat_prompt(
            system_message="Translate natural language text to terminal commands. Respond in the format 'Command: <command>'",
            user_messages=[
                f"Platform: {sys.platform}",
                f"Natural language text text: {text}",
            ],
            model="gpt-3.5-turbo"
        )
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)


def process_command(command):
    command = command.strip()
    if command.startswith("Command:"):
        command = command[8:].strip()
    if command.startswith("```") and command.endswith("```"):
        command = command[3:-3].strip()
    if command.startswith("`") and command.endswith("`"):
        command = command[1:-1].strip()
    return command


def main(input_string):
    translated_command = translate_to_terminal_command(input_string).strip()
    translated_command = process_command(translated_command)
    print(translated_command)
    try:
        pyperclip.copy(translated_command)
    except pyperclip.PyperclipException:
        pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cmd.py <input_string>")
        sys.exit(1)
    
    main(sys.argv[1])