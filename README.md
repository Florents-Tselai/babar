<p align="center">
<p align="center">
   <img width="50%" height="40%" src="https://tselai.com/data/babar-1.png" alt="Logo">
  </p>
  <h1 align="center">Babar🐘❤️🐍</h1>
  <p align="center">
  <strong>Turn any Python object into a Postgres extension</strong>
    <br> <br />
    <a href="#status"><strong> Status</strong></a> |
    <a href="#why"><strong> Why</strong></a> |
    <a href="#how"><strong> How </strong></a> |
    <a href="#installation"><strong> Installation </strong></a> |
    <a href="#usage"><strong> Usage </strong></a> |
    <a href="#roadmap"><strong> Roadmap </strong></a> 

   </p>
<p align="center">

<p align="center">
<a href="https://pypi.org/project/pybabar/"><img src="https://img.shields.io/pypi/v/pybabar?label=PyPI"></a>
<a href="https://github.com/Florents-Tselai/babar/actions/workflows/test.yml?branch=mainline"><img src="https://github.com/Florents-Tselai/babar/actions/workflows/test.yml/badge.svg"></a>
<a href="https://codecov.io/gh/florents-tselai/babar"><img src="https://codecov.io/gh/Florents-Tselai/babar/branch/main/graph/badge.svg"></a>  
<a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
<a href="https://github.com/Florents-Tselai/babar/releases"><img src="https://img.shields.io/github/v/release/Florents-Tselai/babar?include_prereleases&label=changelog"></a>

## Status

WARNING: This is a work in progress and is far from doing what it promises.
But not that far... 😉

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

Let's create a Postgres extension called [`pystring`](babar/examples/pystring.py)
which adds a few Python functions.

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
