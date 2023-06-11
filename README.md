# resmgt

A silly little resource management / city building / survival / 4X game.

## Installation

Requires:

- [python 3](https://www.python.org/downloads/) (tested on 3.9)
- [postgres](https://www.postgresql.org/download/) (tested on 15.3)

### python 3

Most computers come with python 3 nowadays.

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

### postgres

Windows: run installer `.exe`

During installation, provide:

- a superuser password for the `postgres` user
- a port, default `5432`

Enter these into a `.env` file as follows:

```.env
PGHOST="localhost"
PGPORT=5432
PGDATABASE="resmgt"
PGUSER="postgres"
PGPASSWORD="<password>"
```

where `PGDATABASE="resmgt"` is the name of the database to use/create for the game.

On Windows, you may need to add `C:\Program Files\PostgreSQL\{version}\bin` to your `Path` manually in environment variables.

## Tests

Testing is provided via `unittest`. Run:

```bash
python3 -m unittest discover tests
```
