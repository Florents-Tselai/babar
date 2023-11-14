from click.testing import CliRunner
from babar.cli import cli
import pytest


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.output.startswith("Usage:")


def test_files_created():
    pass
