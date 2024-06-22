"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""

import contextlib
import platform
import shutil
import webbrowser
from pathlib import Path

from invoke import task

ROOT_DIR = Path(__file__).parent
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("messagebus/tests")
SOURCE_DIR = ROOT_DIR.joinpath("messagebus")
TOX_DIR = ROOT_DIR.joinpath(".tox")
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")
COVERAGE_REPORT = COVERAGE_DIR.joinpath("index.html")
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]


def _delete_file(file):
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        with contextlib.suppress(FileNotFoundError):
            file.unlink()


def _run(c, command):
    return c.run(command, pty=platform.system() != "Windows")


@task(help={"check": "Checks if source is formatted without applying changes"})
def format(c, check=False):  # noqa: FBT002
    """
    Format code
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    # Run ruff format
    _run(c, f"ruff format {python_dirs_string}")
    # Run isort
    isort_options = "{}".format("--check-only --diff" if check else "")
    _run(c, f"isort {isort_options} {python_dirs_string}")


@task
def lint_ruff(c):
    """
    Lint code with ruff
    """
    cmd = "ruff check {}".format(" ".join(PYTHON_DIRS))
    print(f"CMD!\n{cmd}")
    _run(c, cmd)


@task(lint_ruff)
def lint(c):
    """
    Run all linting
    """


@task
def test(c):
    """
    Run tests
    """
    _run(c, "pytest")


@task(help={"publish": "Publish the result via coveralls"})
def coverage(c, publish=False):
    """
    Create coverage report
    """
    _run(c, f"coverage run --source {SOURCE_DIR} -m pytest")
    _run(c, "coverage report")
    if publish:
        # Publish the results via coveralls
        _run(c, "coveralls")
    else:
        # Build a local report
        _run(c, "coverage html")
        webbrowser.open(COVERAGE_REPORT.as_uri())


@task(help={"launch": "Launch documentation in the web browser"})
def docs(c, launch=True):
    """
    Generate documentation
    """
    _run(c, f"sphinx-build -b html {DOCS_DIR} {DOCS_BUILD_DIR}")
    if launch:
        webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_docs(c):
    """
    Clean up files from documentation builds
    """
    _run(c, f"rm -fr {DOCS_BUILD_DIR}")


@task
def clean_build(c):
    """
    Clean up files from package building
    """
    _run(c, "rm -fr build/")
    _run(c, "rm -fr dist/")
    _run(c, "rm -fr .eggs/")
    _run(c, "find . -name '*.egg-info' -exec rm -fr {} +")
    _run(c, "find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(c):
    """
    Clean up python file artifacts
    """
    _run(c, "find . -name '*.pyc' -exec rm -f {} +")
    _run(c, "find . -name '*.pyo' -exec rm -f {} +")
    _run(c, "find . -name '*~' -exec rm -f {} +")
    _run(c, "find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(c):
    """
    Clean up files from testing
    """
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(TOX_DIR, ignore_errors=True)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(c):
    """
    Runs all clean sub-tasks
    """


@task(clean)
def dist(c):
    """
    Build source and wheel packages
    """
    _run(c, "poetry build")


@task(pre=[clean, dist])
def release(c):
    """
    Make a release of the python package to pypi
    """
    _run(c, "poetry publish")
