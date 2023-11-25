""" Test type hints -> Postgres types (sql) conversion """
import pytest
from babar.pg import PgFunction, PgType, PgSignature, PgParameter
import inspect
from babar import error
from collections import OrderedDict
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
