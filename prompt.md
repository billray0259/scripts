File Structure:
src/autocontext.py
src/cli.py
src/lib/file_data_bundle.py
src/lib/openai_lib.py
src/lib/util.py
src/prompt.py
src/summarize.py

src/autocontext.py
```
import sys

import openai
import lib.openai_lib as openai_lib
from prompt import tree_str, files_str


def context_files(file_structure, instructions):
    try:
        openai.api_key = openai_lib.get_api_key()
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

    print(file_structure)

    try:
        response = openai_lib.chat_prompt(
            system_message="You are a context provider. You identify files in a directory that are neccessary for a developer to see while attempting to complete the user's instructions. The developer will only be able to see the file structure, the contents of the files you identify, and the user's instructions. Identify the relative file paths of the files the developer needs to be able to see. You must respond in the format ```/<file_path>\n/<file_path>\n.../<file_path>``` where '/' is the root direcotry. Do not include any other text.",
            user_messages=[
                f"File structure:\n{file_structure}",
                f"Instructions:\n{instructions}",
            ],
            model="gpt-4"
        )
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

    response = response.strip()
    if response.startswith("```") and response.endswith("```"):
        response = response[3:-3].strip()
    
    return response.splitlines()


# for every file, read it and summarize it. Return a dictionary of file paths to summaries
def summarize_files(files):
    try:
        openai.api_key = openai_lib.get_api_key()
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

    summaries = {}
    for file in files:
        with open(file, "r") as f:
            contents = f.read()
        
        try:
            response = openai_lib.chat_prompt(
                system_message="You are a thorough but concise summarizer. A developer, who is trying to complete a user's instructions, but knows nothing about this project, will read your summary and then decide if they need to read the entire file to complete the instructions. Make your summary as useful as possible to the developer while respecting the developer's time (don't write any more than is necessary). Do not include any other text apart from your summary.",
                user_messages=[
                    f"File contents:\n{contents}",
                ],
                model="gpt-4"
            )
        except Exception as e:
            print("Error: ", e)
            sys.exit(1)

        response = response.strip()
        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
        
        summaries[file] = response

    return summaries


def main(current_directory, instructions):
    print(current_directory)
    file_structure = tree_str(current_directory)
    files = context_files(file_structure, instructions)
    print(files)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python context.py <current_directory> <instructions>")
        sys.exit(1)
    
    # main(sys.argv[1], sys.argv[2])
    import json
    summaries = summarize_files(["src/prompt.py", "commands/prompt"])
    print(json.dumps(summaries, indent=4))
```

src/summarize.py
```
import sys

import openai
import tiktoken

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
        
        try:
            response = openai_lib.chat_prompt(
                system_message="You are a thorough but concise summarizer. A developer, who is trying to complete a user's instructions, but knows nothing about this project, will read your summary and then decide if they need to read the entire file to complete the instructions. Make your summary as useful as possible to the developer while respecting the developer's time (don't write any more than is necessary). Do not include any other text apart from your summary.",
                user_messages=[
                    f"File contents:\n{contents}",
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
    if len(sys.argv) < 3:
        print("Usage: python summarize.py <directory> <output_file> [model]")
        sys.exit(1)
    
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2])
```

src/cli.py
```
import sys
import openai
import pyperclip

import lib.openai_lib as openai_lib


def translate_to_terminal_command(text):
    try:
        openai.api_key = openai_lib.get_api_key()
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)

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
```

src/prompt.py
```
import sys
import tiktoken

from lib.file_data_bundle import FileDataBundle


def prompt_gen(directory, ignore=None):
    """Generates a string with the file structure of the specified directory, and all of the file contents in the format:
    <file_structure>
    
    <file_path>
    ```
    <file_contents>
    ```

    <file_path>
    ```
    <file_contents>
    ```
    ...
    """

    file_bundle = FileDataBundle.bundle_directory(directory)

    if ignore is not None:
        file_bundle.pop(ignore, None)
    
    files = list(file_bundle.keys())
    files.sort()
    files_str = "\n".join(files)
    return f"File Structure:\n{files_str}\n\n{str(file_bundle)}"


def main(source_dir, target_file):
    prompt = prompt_gen(source_dir, ignore=target_file)
    with open(target_file, "w") as f:
        f.write(prompt)
    
    gpt4_encoding = tiktoken.encoding_for_model("gpt-4")
    print(f"GPT-4 prompt length: {len(gpt4_encoding.encode(prompt))}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python prompt.py <source_dir> <target_file>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
```

src/lib/openai_lib.py
```
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
```

src/lib/util.py
```
import os
import subprocess
import re


def find_files(directory, relative_path=True, ignore_pycache=True):
    """Return a list of all files under 'directory' and its subdirectories."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        if ignore_pycache and "__pycache__" in dirs:
            dirs.remove("__pycache__")
            
        for filename in filenames:
            if relative_path:
                filename = os.path.relpath(os.path.join(root, filename), directory)
            else:
                filename = os.path.join(root, filename)
            files.append(filename)
    return files


def tree_str(directory):
    """Runs the tree command on the specified directory and returns the output."""
    tree = subprocess.run(["tree", "-C", directory], stdout=subprocess.PIPE)
    output = tree.stdout.decode("utf-8")
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ".\n" + "\n".join(ansi_escape.sub('', output).splitlines()[1:-2])
```

src/lib/file_data_bundle.py
```
from lib.util import find_files


class FileDataBundle(dict):
    def __init__(self, bundle):
        # data is a dictionary of file paths to file contents
        super().__init__(bundle)


    # static method to load from a file
    @staticmethod
    def load(input_file):
        bundle = {}
        with open(input_file, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 3):
                file_path = lines[i].strip()
                bundle[file_path] = lines[i+2].strip()
        return FileDataBundle(bundle)
    

    @staticmethod
    def bundle_directory(directory):
        bundle = {}
        for file in find_files(directory, relative_path=False):
            try:
                with open(file, "r") as f:
                    bundle[file] = f.read()
            except UnicodeDecodeError:
                # count how many bytes are in the file
                with open(file, "rb") as f:
                    f.seek(0, 2)
                    num_bytes = f.tell()
                    bundle[file] = f"Binary file with {num_bytes} bytes"
        return FileDataBundle(bundle)


    def save(self, output_file):
        with open(output_file, "w") as f:
            f.write(str(self))
    

    def __str__(self):
        string = ""
        for file_path, contents in self.items():
            string += f"{file_path}\n"
            string += "```\n"
            string += contents
            string += "\n```\n\n"
        return string

```

