from setuptools import setup, find_packages
import os

VERSION = "0.1.0a3"
SHORT_DESCRIPTION = (
    "babar is a library "
    "for automatically generating Postgres extensions "
    "from absolutely any Python object."
)


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="pybabar",
    description=SHORT_DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Florents Tselai",
    author_email="florents@tselai.com",
    url="https://github.com/Florents-Tselai/babar",
    project_urls={
        "Documentation": "https://github.com/Florents-Tselai/babar",
        "Issues": "https://github.com/Florents-Tselai/babar/issues",
        "CI": "https://github.com/Florents-Tselai/babar/actions",
        "Changelog": "https://github.com/Florents-Tselai/babar/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=find_packages(),
    entry_points="""
        [console_scripts]
        babar=babar.cli:cli
    """,
    install_requires=[
        "click",
        "click-default-group>=1.2.3",
        "pydantic>=1.10.2",
        "setuptools",
        "pip",
    ],
    extras_require={"test": ["pytest", "pytest-cov", "black", "ruff", "click"]},
    python_requires=">=3.7",
)
