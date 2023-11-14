import click
from click_default_group import DefaultGroup
from dataclasses import asdict

import shutil


@click.group(
    cls=DefaultGroup,
    default="create",
    default_if_no_args=True,
)
@click.version_option()
def cli():
    """
    Create a Postgres extension from absolutely any Python object.

    """
