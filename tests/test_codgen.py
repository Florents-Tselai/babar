import pytest
from babar.pg import PgFunction, PgType, PgSignature, PgParameter
import inspect
from babar import error
from collections import OrderedDict


def test_nohints_raises_error(pyaddint_nohints):
    with pytest.raises(error.NoTypeHintsDetected):
        raise error.NoTypeHintsDetected


def test_raises_error_pg_keyword():
    pass


def test_pgfunction_body(pgfunc):
    assert (
        pgfunc.body
        == r"""def pyconcat(x: str, y: str) -> str:
    return x + y

return pyconcat(x,y)"""
    )


def test_pgfunction_creation(pgfunc):
    assert type(pgfunc) == PgFunction
    assert pgfunc.name == "pyconcat"

    assert (
        pgfunc.sql
        == r"""create function pyconcat(x text, y text) returns text
language plpython3u as
$$
def pyconcat(x: str, y: str) -> str:
    return x + y

return pyconcat(x,y)
$$;"""
    )
