import pathlib
import shutil
from itertools import chain

import nox

ROOT = pathlib.Path(__file__).parent


@nox.session(name="test-with-pip", python=["3.10", "3.11", "3.12"])
def test_with_pip(session: nox.Session) -> None:
    """Run the tests."""
    session.install("-r", "requirements-testing.in")
    session.install(".")

    session.run("pytest", "--cov=src/bmi_wavewatch3", "-vvv")
    session.run("coverage", "report", "--ignore-errors", "--show-missing")
    # "--fail-under=100",


@nox.session(
    name="test-with-conda", venv_backend="mamba", python=["3.10", "3.11", "3.12"]
)
def test_with_conda(session: nox.Session) -> None:
    """Run the tests."""
    session.conda_install("--file=requirements-testing.in")
    session.conda_install("--file=requirements-conda.in")
    session.install(".", "--no-deps")

    session.run("pytest", "--cov=src/bmi_wavewatch3", "-vvv")
    session.run("coverage", "report", "--ignore-errors", "--show-missing")
    # "--fail-under=100",


@nox.session
def cli(session: nox.Session) -> None:
    """Test the command line interface."""
    session.install(".")
    session.run("ww3", "--version")
    session.run("ww3", "--help")
    session.run("ww3", "clean", "--help")
    session.run("ww3", "fetch", "--help")
    session.run("ww3", "info", "--help")
    session.run("ww3", "plot", "--help")
    session.run("ww3", "url", "--help")


@nox.session
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def towncrier(session: nox.Session) -> None:
    """Check that there is a news fragment."""
    session.install("towncrier")
    session.run("towncrier", "check", "--compare-with", "origin/main")


@nox.session(python="3.9", venv_backend="conda")
def locks(session: nox.Session) -> None:
    """Create requirement lock files."""
    session.install("pip-tools")
    with open("requirements.txt", "wb") as fp:
        session.run("pip-compile", "--upgrade", "pyproject.toml", stdout=fp)

    # session.install("conda-lock")
    # session.run("conda-lock", "lock", "--mamba", "--kind=lock", "-f", "pyproject.toml")


@nox.session(name="sync-requirements", python="3.11", venv_backend="conda")
def sync_requirements(session: nox.Session) -> None:
    """Sync requirements.in with pyproject.toml."""
    pypi_mapping = {"ecmwflibs": "findlibs"}

    with open("requirements.in", "w") as fp:
        session.run(
            "python",
            "-c",
            """
import os, tomllib
with open("pyproject.toml", "rb") as fp:
    print(os.linesep.join(sorted(tomllib.load(fp)["project"]["dependencies"])))
""",
            stdout=fp,
        )

    with open("requirements.in") as fp:
        pypi_requirements = set(fp.read().splitlines())

    with open("requirements-conda.in", "w") as fp:
        for requirement in sorted(
            {pypi_mapping.get(req, req) for req in pypi_requirements}
        ):
            print(requirement, file=fp)


@nox.session
def docs(session: nox.Session) -> None:
    """Build the docs."""
    build_dir = ROOT / "build"
    docs_dir = ROOT / "docs"

    clean_docs(session)

    session.install("-r", docs_dir / "requirements.txt")
    session.install("-e", ".")

    session.run(
        "sphinx-apidoc", "--force", "-o", docs_dir / "source/api", "src/bmi_wavewatch3"
    )

    build_dir.mkdir(exist_ok=True)
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-W",
        "--keep-going",
        docs_dir / "source",
        build_dir / "html",
    )


@nox.session
def build(session: nox.Session) -> None:
    """Build sdist and wheel dists."""
    session.install("pip")
    session.install("wheel")
    session.install("setuptools")
    session.run("python", "--version")
    session.run("pip", "--version")
    session.run(
        "python", "setup.py", "bdist_wheel", "sdist", "--dist-dir", "./wheelhouse"
    )


@nox.session
def release(session):
    """Tag, build and publish a new release to PyPI."""
    session.install("zest.releaser[recommended]")
    session.install("zestreleaser.towncrier")
    session.run("fullrelease")


@nox.session
def publish_testpypi(session):
    """Publish wheelhouse/* to TestPyPI."""
    session.run("twine", "check", "wheelhouse/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "--repository-url",
        "https://test.pypi.org/legacy/",
        "wheelhouse/*.tar.gz",
    )


@nox.session
def publish_pypi(session):
    """Publish wheelhouse/* to PyPI."""
    session.run("twine", "check", "wheelhouse/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "wheelhouse/*.tar.gz",
    )


@nox.session(python=False)
def clean(session):
    """Remove all .venv's, build files and caches in the directory."""
    PROJECT = "bmi_wavewatch3"
    ROOT = pathlib.Path(__file__).parent

    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("wheelhouse", ignore_errors=True)
    shutil.rmtree(f"src/{PROJECT}.egg-info", ignore_errors=True)
    shutil.rmtree(".pytest_cache", ignore_errors=True)
    shutil.rmtree(".venv", ignore_errors=True)
    for p in chain(ROOT.rglob("*.py[co]"), ROOT.rglob("__pycache__")):
        if p.is_dir():
            p.rmdir()
        else:
            p.unlink()


@nox.session(python=False, name="clean-docs")
def clean_docs(session: nox.Session) -> None:
    """Clean up the docs folder."""
    if (ROOT / "build" / "html").exists():
        with session.chdir(ROOT / "build"):
            shutil.rmtree("html")
