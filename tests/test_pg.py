import os.path

"Tests extension files (.control, .sql, Makefile) are created and populated properly"


def test_control_file(ext, user_path):
    assert ext.name == "pystring"
    # control params are passed correctly
    assert ext.control.comment == "this is the pystring extension"
    assert ext.control.default_version == "0.1.0"

    # defaults are set properly
    assert ext.control.superuser
    assert not ext.control.trusted
    assert not ext.control.relocatable

    assert ext.control_filename == "pystring.control"
    assert ext.control_file.payload.splitlines() == [
        "default_version = '0.1.0'",
        "comment = 'this is the pystring extension'",
        "superuser = true",
        "requires = 'plpython3u'",
    ]

    assert os.path.exists(user_path / "pystring.control")


def test_makefile_file(ext, user_path):
    assert ext.makefile.name_prefix == "Makefile"

    assert ext.makefile.payload.splitlines() == [
        "EXTENSION = pystring",
        "DATA = pystring--0.1.0.sql",
        "PG_CONFIG = pg_config",
        "PGXS := $(shell $(PG_CONFIG) --pgxs)",
        "include $(PGXS)",
    ]

    assert os.path.exists(user_path / ext.makefile_filename)


def test_sql_file(ext, user_path):
    assert ext.sql_file.name_prefix == "pystring--0.1.0.sql"
    assert ext.sql_file._components[0].sql.startswith("create function")
    assert ext.sql_file.payload.startswith("create function")
    assert os.path.exists(user_path / "pystring--0.1.0.sql")


def test_ext_tarfile(ext, user_path):
    pass
    # assert os.path.exists(user_path / ext.tar_filename)


def test_nohints_raises_error(pyaddint_nohints):
    with pytest.raises(error.NoTypeHintsDetected):
        raise error.NoTypeHintsDetected


def test_raises_error_pg_keyword():
    pass


def test_pgfunction_creation():
    pgfunc = PgFunction(pyconcat)
    assert pgfunc.name == "pyconcat"

    assert (
            pgfunc.sql
            == r"""create function pyconcat(x text, y text) returns text
language plpython3u as
$$
from typing import List, Iterable

def pyconcat(x: str, y: str) -> str:
    return x + y

return pyconcat(x,y)
$$;"""
    )


import pytest
from babar.examples.pystring import *

""" Coversion Python function Signature --> Postgres function signature"""


def test_pgsignature_all_str():
    pysig = inspect.signature(pyconcat)
    pyparams = pysig.parameters

    assert PgParameter.from_pyparameter(pyparams["x"]).name == "x"
    assert PgParameter.from_pyparameter(pyparams["x"]).type_.sql == "text"

    assert PgParameter.from_pyparameter(pyparams["y"]).name == "y"
    assert PgParameter.from_pyparameter(pyparams["y"]).type_.sql == "text"

    pgsign = PgSignature.from_callable(pyconcat)

    assert len(pgsign.parameters) == 2

    assert pgsign.parameters == OrderedDict(
        x=PgParameter("x", PgType(str)), y=PgParameter("y", PgType(str))
    )

    assert pgsign.ret_type == PgType(str)

    assert pgsign.sql == "(x text, y text) returns text"


@pytest.mark.parametrize(
    "func, ret_sql",
    [
        (pyconcat, "text"),
        (pystrlen, "int"),
        (pystrsplit, "text[]"),
        (pyisdigit, "boolean"),
    ],
)
def test_return_type(func, ret_sql):
    pgsign = PgSignature.from_callable(func)
    assert pgsign.ret_type.sql == ret_sql


# def test_pyformat():
#     from babar.examples.pystring import pyformat
#
#     assert pyformat("The sum of 1 + 2 is {0}", 1 + 2) == "The sum of 1 + 2 is 3"

""" Test type hints -> Postgres types (sql) conversion """
import pytest
from typing import *


@pytest.mark.parametrize(
    "pytype, exp_pgtype",
    [
        (str, "text"),
        (int, "int"),
        (float, "float"),
        (bool, "boolean"),
        (List[str], "text[]"),
        (Iterable[str], "text[]"),
        (Sequence[str], "text[]"),
        (List[int], "int[]"),
        (Iterable[int], "int[]"),
        (Sequence[int], "int[]"),
        (List[float], "float[]"),
        (Iterable[float], "float[]"),
        (Sequence[float], "float[]"),
    ],
)
def test_py_to_pg_conversion(pytype, exp_pgtype):
    # TODO: this should probably be a factory. Need to figure out the proper class design
    assert PgType(pytype).sql == exp_pgtype


import pytest
from babar.pg import PgFunction, PgType, PgSignature, PgParameter
import inspect
from babar import error
from collections import OrderedDict
from babar.examples.pystring import pyconcat


def test_nohints_raises_error(pyaddint_nohints):
    with pytest.raises(error.NoTypeHintsDetected):
        raise error.NoTypeHintsDetected


def test_raises_error_pg_keyword():
    pass


def test_pgfunction_creation():
    pgfunc = PgFunction(pyconcat)
    assert pgfunc.name == "pyconcat"

    assert (
            pgfunc.sql
            == r"""create function pyconcat(x text, y text) returns text
language plpython3u as
$$
from typing import List, Iterable

def pyconcat(x: str, y: str) -> str:
    return x + y

return pyconcat(x,y)
$$;"""
    )


"Tests extension files (.control, .sql, Makefile) are created and populated properly"


def test_control_file(ext, user_path):
    assert ext.name == "pystring"
    # control params are passed correctly
    assert ext.control.comment == "this is the pystring extension"
    assert ext.control.default_version == "0.1.0"

    # defaults are set properly
    assert ext.control.superuser
    assert not ext.control.trusted
    assert not ext.control.relocatable

    assert ext.control_filename == "pystring.control"
    assert ext.control_file.payload.splitlines() == [
        "default_version = '0.1.0'",
        "comment = 'this is the pystring extension'",
        "superuser = true",
        "requires = 'plpython3u'",
    ]

    assert os.path.exists(user_path / "pystring.control")


def test_makefile_file(ext, user_path):
    assert ext.makefile.name_prefix == "Makefile"

    assert ext.makefile.payload.splitlines() == [
        "EXTENSION = pystring",
        "DATA = pystring--0.1.0.sql",
        "PG_CONFIG = pg_config",
        "PGXS := $(shell $(PG_CONFIG) --pgxs)",
        "include $(PGXS)",
    ]

    assert os.path.exists(user_path / ext.makefile_filename)


def test_sql_file(ext, user_path):
    assert ext.sql_file.name_prefix == "pystring--0.1.0.sql"
    assert ext.sql_file._components[0].sql.startswith("create function")
    assert ext.sql_file.payload.startswith("create function")
    assert os.path.exists(user_path / "pystring--0.1.0.sql")


def test_ext_tarfile(ext, user_path):
    pass
    # assert os.path.exists(user_path / ext.tar_filename)
