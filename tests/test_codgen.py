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


@pytest.mark.parametrize(
    "pytype, exp_pgtype",
    [(str, "text"), (int, "int"), (float, "float"), (bool, "boolean")],
)
def test_py_to_pg_conversion(pytype, exp_pgtype):
    # TODO: this should probably be a factory. Need to figure out the proper class design
    assert PgType(pytype).sql == exp_pgtype


""" Coversion Python function Signature --> Postgres function signature"""


def test_pgsignature(pyconcat):
    def f(x: str, y: str) -> str:
        pass

    pysig = inspect.signature(f)
    pyparams = pysig.parameters

    assert PgParameter.from_pyparameter(pyparams["x"]).name == "x"
    assert PgParameter.from_pyparameter(pyparams["x"]).type_.sql == "text"

    assert PgParameter.from_pyparameter(pyparams["y"]).name == "y"
    assert PgParameter.from_pyparameter(pyparams["y"]).type_.sql == "text"

    pgsign = PgSignature.from_callable(f)

    assert len(pgsign.parameters) == 2

    assert pgsign.parameters == OrderedDict(
        x=PgParameter("x", PgType(str)), y=PgParameter("y", PgType(str))
    )
    assert pgsign.sql == "(x text, y text) returns text"


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
