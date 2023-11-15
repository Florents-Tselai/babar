from babar import Extension


def pyconcat(x: str, y: str) -> str:
    return x + y


def pyupper(x: str) -> str:
    return x.upper()


if __name__ == "__main__":
    Extension(
        "pystring",
        pyconcat,
        pyupper,
        comment="this is the pystring extension",
        default_version="0.1.0",
    )
