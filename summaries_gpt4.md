commands/autocontext
```
This Bash script sets the path to a virtual environment, activates it, concatenates all command-line arguments, gets the current directory, and runs the 'autocontext.py' script with the concatenated input string in the current directory. Afterward, it deactivates the virtual environment.
```

commands/cli
```
This Bash script activates a Python virtual environment, concatenates all command-line arguments, runs a `cli.py` script using the input string, and deactivates the virtual environment.
```

commands/prompt
```
This script activates a virtual environment and runs a Python script (prompt.py) with two optional arguments, source_directory and target_file. If provided, source_directory and target_file define the source directory and output file, respectively. An error occurs if more than two arguments are given. The virtual environment is deactivated after the script runs.
```

