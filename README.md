<p align="center">
<p align="center">
   <img width="250" height="250" src="https://tselai.com/data/babar-1.png" alt="Logo">
  </p>
  <h1 align="center">Babar🐘❤️🐍</h1>
  <p align="center">
  <strong>Turn any Python object into a Postgres extension</strong>
    <br> <br />
    <a href="#why"><strong> Why</strong></a> |
    <a href="#how"><strong> How </strong></a> |
    <a href="#installation"><strong> Installation </strong></a> |
    <a href="#usage"><strong> Usage </strong></a> |
    <a href="#roadmap"><strong> Roadmap </strong></a> 

   </p>

## Why

Postgres has supported Python as a procedural language for years
via [PL/Python](https://www.postgresql.org/docs/current/plpython.html).

Embedding non-trivial Python code in Postgres  can get cumbersome and usually
involves copy-pasting from existing code bases and/or creating thin wrappers around existing functions.

**babar** automates this process by allowing you to seamlessly package existing Python components (functions, classes etc.)
int a postgres extension.

## How
**babar** dynamically inspects the definition of Python objects
and generates semantically equivalent Postgres definitions
along with the necessary extension files (`.control`, `Makefile`, `.sql`)

## Installation

## Usage

```bash
pip install pybabar
```

Let's create a Postgres extension called `pystring`
which adds two simple Python functions.

```python
from babar import Extension

def pyconcat(x: str, y: str) -> str:
    return x + y

def pyupper(x: str) -> str:
    return x.upper()

if __name__ == "__main__":
    Extension(
        "pystring",
        pyconcat, pyupper,
        comment="this is the pystring extension",
        default_version="0.1.0",
    )
```

Then, from the command line, you can run:

```bash
python pystring.py
```

That will create the appropriate extension files,
which you can then install in the usual Postgres way:
```bash
make 
make install
```

Then you can `CREATE` the extension and use it

```bash
psql -d postgres <<SQL
CREATE EXTENSION pystring

SELECT pyconcat('hello ', 'world');
SELECT pyupper('hello');
SQL
```

## Roadmap

## v0.1.0 (wip)

* simple functions (not classes, methods etc)
* Functions should be 100% self-contained (outer scope is not inspected)
* primitive types only: support only str/text as arg and return
* Probably no cli interface / just python __main__.py

## Future
* `@pg_function` decorator for individual functions. Much like `click`;
* maybe subclass `Extension` should make a whole Python class an extension?
* CLI like `babar -m pack.mod.func1 pack2.mod2.func2`
* Handle upgrades
* pgxn integration

---

It is lightly inspired by [Python-Fire](https://github.com/google/python-fire) 
which turns any Python object into a cli interface
