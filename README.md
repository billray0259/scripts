Clone this repository to your home directory

add the OPENAI_API_KEY.txt file to the root of the repository with your OpenAI API key

Add this to your .bashrc or .zshrc:
`export PATH="$PATH:$HOME/scripts/commands"`

`chmod +x` the scripts you want to use or `chmod +x commands` if you want to use them all

Setup the virtual environment

```
cd ~/scripts
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
