commands/autocontext
```
This Bash script activates a virtual environment located in `~/scripts/.env`, concatenates all command-line arguments, and stores it in a variable named `instructions`. Then, it gets the current directory, runs a Python script located in `~/scripts/src/autocontext.py` with the concatenated input string and current directory as arguments, and finally deactivates the virtual environment.
```

commands/cli
```
This Bash script activates a virtual environment, concatenates all command-line arguments, passes the concatenated string as an input to a Python script named "cli.py", and then deactivates the virtual environment.
```

commands/prompt
```
This is a Bash script that activates a virtual environment, sets source and target directories and then calls a Python script, prompt.py. The script expects up to two arguments: source_directory and target_directory. If there are no arguments, it will use the current directory as the source directory and "prompt.md" as the target file. If there is one argument, it will use it as the source directory and "prompt.md" as the target file. If there are two arguments, they will be used as the source and target directories. If there are more than two arguments, the script will display an error message. Finally, the script deactivates the virtual environment.
```

