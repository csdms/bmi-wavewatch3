import pathlib

import pytest
from click.testing import CliRunner

from bmi_wavewatch3.cli import ww3

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(ww3, ["--help"])
    assert result.exit_code == 0

    result = runner.invoke(ww3, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


@pytest.mark.parametrize("subcommand", ("url", "fetch"))
@pytest.mark.parametrize(
    "date",
    ["2010", "2010-05", "10-5", "2010-01-32", "2010-25-12", "1776-07-04", "2100-01-01"],
)
def test_bad_date(subcommand, date):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand, date])
    assert result.exit_code != 0


@pytest.mark.parametrize("subcommand", ("url", "fetch", "info"))
def test_bad_source(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, ["--source=foo", subcommand])
    assert result.exit_code != 0


@pytest.mark.parametrize("subcommand", ("url", "fetch"))
def test_bad_quantity(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand, "--quantity=foo"])
    assert result.exit_code != 0


@pytest.mark.parametrize("subcommand", ("url", "fetch"))
def test_bad_grid(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand, "--grid=foo"])
    assert result.exit_code != 0


@pytest.mark.parametrize("subcommand", ("url", "fetch", "clean"))
def test_subcommand_help(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand, "--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize("subcommand", ("url", "fetch"))
def test_noop(subcommand):
    runner = CliRunner()
    result = runner.invoke(ww3, [subcommand])
    assert result.exit_code == 0


def test_info_is_toml():
    runner = CliRunner()
    result = runner.invoke(ww3, ["info"])
    assert result.exit_code == 0
    sections = tomllib.loads(result.stdout)
    assert list(sections) == ["wavewatch3"]
    assert list(sections["wavewatch3"]) == ["sources"]
    assert len(sections["wavewatch3"]["sources"]) == 1

    result = runner.invoke(ww3, ["info", "--all"])
    assert result.exit_code == 0
    sections = tomllib.loads(result.stdout)
    assert list(sections) == ["wavewatch3"]
    assert list(sections["wavewatch3"]) == ["sources"]
    assert len(sections["wavewatch3"]["sources"]) > 1


def test_clean(tmpdir):
    runner = CliRunner()

    with tmpdir.as_cwd():
        data_file = pathlib.Path("multi_1.glo_30m.dp.201712.grb2")
        data_file.touch()

        assert data_file.is_file()
        runner.invoke(ww3, ["clean", "--cache-dir=.", "--dry-run"])
        assert data_file.is_file()

        runner.invoke(ww3, ["clean", "--cache-dir=.", "--yes"])
        assert not data_file.is_file()
