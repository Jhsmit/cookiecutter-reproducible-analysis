"""Module of Invoke test tasks for testing the CODE QUALITY to be invoked from the command line. Try

invoke --list=test

from the command line for a list of all available commands.
"""

import os
from pathlib import Path

from invoke import task
from invoke.context import Context


@task()
def black(command: Context):
    """Runs black (autoformatter) on all .py files recursively"""
    print(
        """
Running Black the Python code formatter
=======================================
"""
    )
    command.run("black .", echo=True)


@task()
def flake8(command: Context):
    """Runs flake8 linter."""
    print(
        """
Running flake8.
Flake8 is a python tool that glues together pycodestyle, pyflakes, 
mccabe, and third-party plugins to check the style and quality of 
some python code. 
=======================================================================
"""
    )
    command.run("flake8 .", echo=True)


@task()
def isort(command: Context):
    """Runs isort (import sorter) on all .py files recursively"""
    print(
        """
Running isort the Python code import sorter
===========================================
"""
    )
    command.run("isort .", echo=True)


@task()
def pylint(command: Context, files: str = "setup.py src hal"):
    """Runs pylint (linter) on all .py files recursively to identify coding errors

    Arguments:
        command {[type]} -- [description]
        files {string} -- A space separated list of files and folders to lint
    """
    # https://stackoverflow.com/questions/22241435/pylint-discard-cached-file-state
    # from astroid import MANAGER
    # MANAGER.astroid_cache.clear()
    print(
        """
Running pylint.
Pylint looks for programming errors, helps enforcing a coding standard,
sniffs for code smells and offers simple refactoring suggestions.
=======================================================================
"""
    )
    command_string = f"pylint {files}"
    command.run(command_string, echo=True)


@task
def mypy(command: Context, files: str = "setup.py src hal"):
    """Runs mypy (static type checker) on all .py files recursively

    Arguments:
        command {[type]} -- [description]
        files {string} -- A space separated list of files and folders to lint
    """
    print(
        """
Running mypy for identifying python type errors
===============================================
"""
    )
    command_string = f"mypy {files}"
    command.run(command_string, echo=True)


def export_env(command: Context,
               filename: str = 'environment.yml',
               override_channels: bool = False,
               no_builds: bool = False,
               ignore_channels: bool = False,
               from_history: bool = False):
    env_name = Path(os.environ["CONDA_PREFIX"]).name
    print(type(command))
    print(env_name)

    output_pth = Path(__file__).parent / "env"
    print(__file__)
    print(output_pth)

    command_string = (
        f"conda env export --name {env_name} --file {output_pth / filename}"
    )

    if override_channels:
        command_string += " -- override-channels"
    if no_builds:
        command_string += " -- no-builds"
    if ignore_channels:
        command_string += " --ignore-channels"
    if from_history:
        command_string += " --from-history"

    command.run(command_string, echo=True)


@task(
    pre=[isort, black, flake8, pylint, mypy],
    aliases=["pre_commit", "test"],
    name="all",
)
def _all(command):  # pylint: disable=unused-argument
    """Runs isort, flake8, black, pylint, mypy and

    Arguments:
        command {[type]} -- [description]
    """
    # If we get to this point all tests listed in 'pre' have passed
    # unless we have run the task with the --warn flag
    if not command.config.run.warn:
        print(
            """
All Tests Passed Successfully
=============================
"""
        )
