import pytest
from click.testing import CliRunner

from wavewatch3.cli import ww3


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(ww3, ["--help"])
    assert result.exit_code == 0

    result = runner.invoke(ww3, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


@pytest.mark.parametrize("subcommand", ("url", "fetch"))
def test_subcommand_help(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand, "--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize("subcommand", ("url", "fetch"))
def test_noop(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand])
    assert result.exit_code == 0
