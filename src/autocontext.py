import sys

import openai
import lib.openai_lib as openai_lib
from lib.file_data_bundle import FileDataBundle
from lib.util import find_files


def identify_context_files(file_structure, summary_bundle, instructions, model="gpt-3.5-turbo"):
    try:
        openai.api_key = openai_lib.get_api_key()
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

    try:
        response = openai_lib.chat_prompt(
            system_message="You are a context provider. You identify files in a directory that are neccessary for a developer to see while attempting to complete the user's instructions. The developer will only be able to see the file structure, the contents of the files you identify, and the user's instructions. Identify the relative file paths of the files the developer needs to be able to see. You must respond in the format ```<file_path>\n<file_path>\n...<file_path>```. Do not provide any explination and do not include any other text apart from the file paths in the format specified.",
            user_messages=[
                f"File structure:\n{file_structure}",
                f"File summaries:\n{summary_bundle}",
                f"Instructions:\n{instructions}",
            ],
            model=model
        )
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)
    
    print()
    print(response)
    print()

    response = response.strip()
    if response.startswith("```") and response.endswith("```"):
        response = response[3:-3].strip()
    
    return response.splitlines()


def main(directory, summary_file, instructions_file, model):
    file_structure = "\n".join(find_files(directory))
    summary_bundle = FileDataBundle.load(summary_file)
    with open(instructions_file, "r") as f:
        instructions = f.read()
    context_files = identify_context_files(file_structure, summary_bundle, instructions, model=model)
    print(context_files)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python context.py <directory> <summary_file> <instructions_file> <model>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])