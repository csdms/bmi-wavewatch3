import os
import pathlib
import shutil
from itertools import chain

import nox

PROJECT = "bmi_wavewatch3"
ROOT = pathlib.Path(__file__).parent


@nox.session
def tests(session: nox.Session) -> None:
    """Run the tests."""
    session.install("pytest")
    session.install(".[testing]")
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


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """Look for lint."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def towncrier(session: nox.Session) -> None:
    """Check that there is a news fragment."""
    session.install("towncrier")
    session.run("towncrier", "check", "--compare-with", "origin/main")


@nox.session(name="build-docs", reuse_venv=True)
def build_docs(session: nox.Session) -> None:
    """Build the docs."""
    with session.chdir(ROOT):
        session.install(".[doc]")

    clean_docs(session)

    with session.chdir(ROOT):
        session.run(
            "sphinx-apidoc",
            "-e",
            "-force",
            "--no-toc",
            "--module-first",
            "--templatedir",
            "docs/source/_templates",
            "-o",
            "docs/source/api",
            "src/bmi_wavewatch3",
        )
        session.run(
            "sphinx-build",
            "-b",
            "html",
            "-W",
            "docs/source",
            "docs/_build/html",
        )


@nox.session(python=False, name="clean-docs")
def clean_docs(session: nox.Session) -> None:
    """Clean up the docs folder."""
    with session.chdir(ROOT / "docs"):
        if os.path.exists("_build"):
            shutil.rmtree("_build")

        for p in pathlib.Path("source/api").rglob("bmi_wavewatch3*.rst"):
            p.unlink()


@nox.session(name="live-docs", reuse_venv=True)
def live_docs(session: nox.Session) -> None:
    session.install(".[doc]")
    session.run(
        "sphinx-autobuild",
        "-b",
        "html",
        "docs/source",
        "docs/_build/html",
        "--open-browser",
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
    for p in chain(
        ROOT.rglob("*.py[co]"), ROOT.rglob("__pycache__"), ROOT.rglob(".DS_Store")
    ):
        if p.is_dir():
            p.rmdir()
        else:
            p.unlink()
