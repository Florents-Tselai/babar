import pytest
from pathlib import Path
from babar import Extension, PgFunction
from babar.examples import pystring
from babar.examples.pystring import *


@pytest.fixture
def user_path(tmpdir):
    dir = tmpdir / "babar"
    dir.mkdir()
    return dir


@pytest.fixture
def pgfunc():
    return PgFunction(pystring.pyconcat)


@pytest.fixture
def pyaddint_nohints():
    def mypyconcat(x, y):
        return x + y

    return mypyconcat


@pytest.fixture
def ext(user_path):
    ext = Extension(
        "pystring",
        pyconcat,
        pyupper,
        pystrlen,
        pystrsplit,
        pyisdigit,
        # pyformat,
        pyjoin,
        workdir=user_path,
        comment="this is the pystring extension",
        default_version="0.1.0",
    )
    return ext
