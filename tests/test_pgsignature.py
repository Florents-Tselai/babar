import pytest
from babar.pg import PgFunction, PgType, PgSignature, PgParameter
import inspect
from babar import error
from collections import OrderedDict
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
