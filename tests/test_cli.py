import pathlib

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


@pytest.mark.parametrize("subcommand", ("url", "fetch", "clean"))
def test_subcommand_help(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand, "--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize("subcommand", ("url", "fetch", "clean"))
def test_noop(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand])
    assert result.exit_code == 0


def test_clean(tmpdir):
    runner = CliRunner()

    with tmpdir.as_cwd():
        data_file = pathlib.Path("multi_1.glo_30m.dp.201712.grb2")
        data_file.touch()

        assert data_file.is_file()
        result = runner.invoke(ww3, ["clean", "--cache-dir=.", "--dry-run"])
        assert data_file.is_file()

        result = runner.invoke(ww3, ["clean", "--cache-dir=."])
        assert not data_file.is_file()
