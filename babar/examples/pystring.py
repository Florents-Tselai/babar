from babar import Extension
from typing import *


def pyconcat(x: str, y: str) -> str:
    return x + y


def pyupper(x: str) -> str:
    return x.upper()


def pystrlen(x: str) -> int:
    return len(x)


def pystrsplit(x: str, sep: str = ",", maxsplit: int = -1) -> List[str]:
    return x.split(sep, maxsplit)


def pyisdigit(x: str) -> bool:
    return x.isdigit()


# def pyformat(x: str, *args, **kwargs) -> str:
#     return x.format(*args, **kwargs)


def pyjoin(x: Iterable[str], sep: str = ",") -> str:
    return sep.join(x)


if __name__ == "__main__":
    Extension(
        "pystring",
        pyconcat,
        pyupper,
        pystrlen,
        pystrsplit,
        pyisdigit,
        # pyformat,
        pyjoin,
        comment="this is the pystring extension",
        default_version="0.1.0",
    )
