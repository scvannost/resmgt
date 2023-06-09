# resmgt

A silly little resource management / city building / survival / 4X game.

## Installation

Requires:

- python 3 (tested on 3.9)

It's suggested to install this game in a virtual environment; to create one run

```bash
python3 -m venv venv
```

Then to activate the venv run:

- Windows: `& venv/Scripts/Activate.ps1`
- Unix: `source venv/scripts/activate`

The venv's name will be prepended to the terminal line. When running, run `deactive` to deactivate it.

To install run:

- `pip install -r requirements.txt` or `pip install -r requirements.dev.txt`

## Tests

Testing is provided via `unittest`. Run:

```bash
python3 -m unittest discover tests
```
