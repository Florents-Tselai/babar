from typing import Callable, Iterator, Union, Optional, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from types import FunctionType
import inspect
from inspect import Signature
from enum import Enum
from textwrap import wrap
from .error import *
from collections import OrderedDict
from copy import copy


class PgObject(ABC):
    """A textual representation of an object as written in an .sql extension file"""

    @staticmethod
    def factory(obj):
        if not hasattr(obj, "__call__"):
            raise ValueError("currently only function are supported")

        if hasattr(obj, "__call__"):
            f = PgFunction(func=obj)
            setattr(f.func, "__name__", obj.__name__)
            return f

    @property
    @abstractmethod
    def sql(self):
        raise NotImplementedError("that's an abstract method")

    def __str__(self):
        return self.sql


@dataclass
class PgType(PgObject):
    types_lookup = dict(
        [(str, "text"), (int, "int"), (float, "float"), (bool, "boolean")]
    )

    pytype: object

    @property
    def sql(self):
        try:
            return self.types_lookup[self.pytype]
        except KeyError:
            raise CannotConvertToPostgresException


@dataclass
class PgParameter(PgObject):
    name: str
    type_: PgType

    @classmethod
    def from_pyparameter(cls, obj: inspect.Parameter):
        return cls(obj.name, PgType(obj.annotation))

    @property
    def sql(self):
        return f"{self.name} {self.type_}"


@dataclass(init=True)
class PgSignature(PgObject):
    """Signature of a Postgres function as inferred by a Python function"""

    pysign: inspect.Signature  # not sure this is the correct hint

    @classmethod
    def from_callable(cls, obj):
        return cls(inspect.signature(obj))

    @property
    def name(self):
        return self.func.__name__

    @property
    def parameters(self):
        return OrderedDict(
            zip(
                self.pysign.parameters.keys(),
                map(PgParameter.from_pyparameter, self.pysign.parameters.values()),
            )
        )

    @property
    def ret_type(self):
        return PgType(str)

    @property
    def sql(self) -> str:
        return (
            f"({', '.join(map(str, self.parameters.values()))}) returns {self.ret_type}"
        )

    def __str__(self):
        return self.sql


@dataclass
class PgFunction(PgObject):
    """CREATE FUNCTION ..."""

    func: Callable  # not sure this is the correct hint

    @property
    def body(self) -> str:
        wrapped = copy(self.func)
        src = inspect.getsource(wrapped)
        src += "\n"
        src += (
            f"return {self.func.__name__}"
            + "("
            + ",".join(PgSignature.from_callable(self.func).parameters.keys())
            + ")"
        )
        return src

    @property
    def name(self):
        return self.func.__name__

    @property
    def sql(self):
        return f"""create function {self.name}{PgSignature.from_callable(self.func)}
language plpython3u as
$$
{self.body}
$$;"""
