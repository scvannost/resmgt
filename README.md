# resmgt

A silly little resource management / city building / survival / 4X game.

## Installation

Requires:

- [python 3](https://www.python.org/downloads/) (tested on 3.13)
- [postgres](https://www.postgresql.org/download/) (tested on 15.3)

### python 3

Most computers come with python 3 nowadays.

It's suggested to install this game in a virtual environment; to create one run

```bash
python -m venv venv
```

Then to activate the venv run:

- Windows: `& venv/Scripts/Activate.ps1`
- Unix: `source venv/scripts/activate`

The venv's name will be prepended to the terminal line. When running, run `deactivate` to deactivate it.

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

Unit testing is provided via `unittest`. Run:

```bash
python -m unittest discover tests
```

Currently, no tests have been implemented so to run the test script:

```bash
python ./test_script.py
```

## Overview

The current pattern for this database-backed game:

1. **`import`ing the `Game` class**:
    1. `connect`s to the default `d[ata]b[ase]` configured by `.env`, `creat[ing it ]if[ it does]n[']t[ ]exist`
    2. sets up a universal list of `sprites`
2. **`init`ializing a `VillagerIconSprite`** only prepares its data
3. **`init`ializing a `Game`**:
    1. `open[s a ]session` on the `d[ata]b[ase]` if needed and `create[s ]all[ the ]tables`
    2. `insert`s the `player[ ]sprite` into the `d[ata]b[ase]`
    3. `add`s the `player[ ]sprite` and any `other[ ]sprites` to the list of `sprites`
    4. `start`s the `Game` (unless passed `start=False`), which itself
        1. `init`ializes `pygame`
        2. sets the `surface` to a `display` of the given `size` (default in `settings`)
        3. sets a new `clock`
        4. sets `running = True`
4. **`run`ning the `Game`** enters the main play loop below
5. **`quit`ting the `Game`**
    1. `quit`s `pygame`
    2. drops the play `surface`
    3. sets `running = False`
6. **it's polite to clean up the `d[ata]b[ase]` by**
    1. `drop[ping ]all[ ]tables`
    2. `drop[ping the ]database` itself (which needs the configuration e.g. from `.env`)
    3. `disconnect`ing

The main play loop `while` a `Game` is `running`:

1. `tick` the `clock`
2. `get` the `pygame` `event`s and `if` any is `type` `QUIT`, set `running = False` (i.e. last round)
3. `get[ the ]pressed` `keys` and `if` `K_ESCAPE`, set `running = False` (i.e. last round)
4. `move` the `player` (`VillagerIconSprite`) based on `pressed_keys`
    1. any `BasicSprite` only `move`s if it has a `speed`
    2. parse the `pressed_keys` onto the unit square as `xy`-coordinates
    3. scale the `xy`-coordinates based on its `speed`
    4. `move[ ]i[n ]p[lace]` the underlying `rect`angle of the `Sprite`
    5. adjust the `rect`angle based on the default `SCREEN_HEIGHT` and `SCREEN_WIDTH`
5. redraw the `Game` board:
    1. `fill`ing the `surface` with the `b[ack]g[round ]color`
    2. `draw`ing each `Group` in the universal `SPRITE_GROUPS`
    3. `flip` i.e. update the `pygame[ ]display`
6. end of loop
    1. `if running` is still truthy, return to step 1
    2. otherwise e.g. after the last round (i.e. `running = False`), exit the loop and `quit` `pygame`

Note in `2` and `3` that setting `running = False` doesn't block the completion of that loop cycle,
but prevents the following repeat from `6.1` to `1`, instead hitting `6.2` and ending the `Game` `run`.

### Notes

#### Database

- all `Game`s must use `postgresql` via `sqlalchemy`
- only `VillagerIconSprite`s are stored in the `database` -- other `Sprite`s don't have `models`
- only the `Villager` `database[ ]models` is used -- the other `Base` sub`class`es are unused
  - of the `Villager`, only the `x` and `y` are used -- other `mapped[ ]column`s and all `relationship`s are unused

#### Design choice

- each `Game` has one `player` (expected to be a `VillagerIconSprite`), which is the only entry in `sprites` that gets to `move`
- the camera is fixed, showing the entire `Game` area
