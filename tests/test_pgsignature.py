import pytest
from babar.pg import PgFunction, PgType, PgSignature, PgParameter
import inspect
from babar import error
from collections import OrderedDict


""" Coversion Python function Signature --> Postgres function signature"""


def test_pgsignature_all_str():
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


def test_return_int():
    from babar.examples.pystring import pystrlen

    pgsign = PgSignature.from_callable(pystrlen)

    assert len(pgsign.parameters) == 1
    assert pgsign.parameters == OrderedDict(x=PgParameter("x", PgType(str)))


def test_pyformat():
    from babar.examples.pystring import pyformat

    assert pyformat("The sum of 1 + 2 is {0}", 1 + 2) == "The sum of 1 + 2 is 3"
