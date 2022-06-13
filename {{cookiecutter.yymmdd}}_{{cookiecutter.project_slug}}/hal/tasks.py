import os
from pathlib import Path
from typing import Optional

from hal.config import cfg
import invoke

context = invoke.Context()


def run_black() -> None:
    command_string = f"black {cfg.paths.src}"
    context.run(command_string, echo=True)


def run_mypy() -> None:
    command_string = f"mypy {cfg.paths.src}"
    context.run(command_string, echo=True)


def run_flake8() -> None:
    command_string = f"flake8 {cfg.paths.src}"
    context.run(command_string, echo=True)


def run_pylint() -> None:
    command_string = f"pylint {cfg.paths.src}"
    context.run(command_string, echo=True)


def run_isort() -> None:
    command_string = f"isort --profile black {cfg.paths.src}"
    context.run(command_string, echo=True)

def export_env(
               filename: Optional[str] = None,
               override_channels: bool = False,
               no_builds: bool = False,
               ignore_channels: bool = False,
               from_history: bool = False):

    env_name = Path(os.environ["CONDA_PREFIX"]).name

    filename = filename or f"{env_name}.yaml"

    output_pth = cfg.paths.root / "env"

    command_string = (
        f"conda env export --name {env_name} --file {output_pth / filename}"
    )

    if override_channels:
        command_string += " --override-channels"
    if no_builds:
        command_string += " --no-builds"
    if ignore_channels:
        command_string += " --ignore-channels"
    if from_history:
        command_string += " --from-history"

    context.run(command_string)

