import os
import subprocess
import re


def find_files(directory, relative_path=True):
    """Return a list of all files under 'directory' and its subdirectories."""
    files = []
    for root, dirs, filenames in os.walk(directory):
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