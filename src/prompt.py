import sys
import os
import subprocess
import re


def find_files(directory):
    """Return a list of all files under 'directory' and its subdirectories."""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files


def tree_str(directory):
    """Runs the tree command on the specified directory and returns the output."""
    tree = subprocess.run(["tree", "-C", directory], stdout=subprocess.PIPE)
    output = tree.stdout.decode("utf-8")
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', output)


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
    
    files = find_files(directory)
    
    prompt = ".\n" + "\n".join(tree_str(directory).splitlines()[1:-2])
    prompt += "\n\n"
    for file in files:
        with open(file, "r") as f:
            contents = f.read()

        relative_path = os.path.relpath(file, directory)
        
        prompt += f"{relative_path}\n"
        prompt += "```\n"
        prompt += contents
        prompt += "\n```\n\n"
    return prompt


source_dir = sys.argv[1]
target_file = sys.argv[2]

prompt = prompt_gen(source_dir, target_file)
with open(target_file, "w") as f:
    f.write(prompt)


import tiktoken
# print number of tokens in prompt
encoding4 = tiktoken.encoding_for_model("gpt-4")
print(f"GPT-4 prompt length: {len(encoding4.encode(prompt))}")