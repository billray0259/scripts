import sys
import os

import openai

import lib.openai_lib as openai_lib
from lib.util import find_files
from lib.file_data_bundle import FileDataBundle



# for every file, read it and summarize it. Return a dictionary of file paths to summaries
def summarize_files(files, model="gpt-3.5-turbo"):
    try:
        openai.api_key = openai_lib.get_api_key()
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

    summaries = {}
    for file in files:
        print(f"Summarizing {file}...")
        with open(file, "r") as f:
            contents = f.read()
        basename = os.path.basename(file)
        try:
            response = openai_lib.chat_prompt(
                system_message="You are a thorough but concise summarizer. A developer, who is trying to complete a user's instructions, but knows nothing about this project, will read your summary and then decide if they need to read the entire file to complete the instructions. Make your summary as useful as possible to the developer while respecting the developer's time (don't write any more than is necessary). Do not include any other text apart from your summary.",
                user_messages=[
                    f"{basename} file contents:\n```{contents}\n```",
                ],
                model=model
            )
        except Exception as e:
            print("Error: ", e)
            sys.exit(1)

        response = response.strip()
        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
        
        summaries[file] = response

    return summaries


def main(directory, output_file, model="gpt-3.5-turbo"):
    files = find_files(directory, relative_path=False)
    summaries = summarize_files(files, model=model)
    bundle = FileDataBundle(summaries)
    bundle.save(output_file)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python summarize.py <directory> <output_file> <model>")
        sys.exit(1)
    

    main(sys.argv[1], sys.argv[2], sys.argv[3])