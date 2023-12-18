Clone this repository to your home directory

Create a `.env` file containing the text `OPENAI_API_KEY=your_key_here`

Add this to your .bashrc or .zshrc:
`export PATH="$PATH:$HOME/scripts/commands"`

`chmod +x` the scripts you want to use or `chmod +x commands` if you want to use them all

Setup the virtual environment

```
cd ~/scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
