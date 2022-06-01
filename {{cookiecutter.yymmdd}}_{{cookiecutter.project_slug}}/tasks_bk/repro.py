# todo change to tasks.py file

import os
from pathlib import Path

print(os.environ["CONDA_PREFIX"])

from invoke import task


@task
def env_export(command):
    env_name = Path(os.environ["CONDA_PREFIX"]).name

    print(env_name)

    output_pth = Path(__file__).parent.parent / "env"

    command_string = (
        f"conda env export --name {env_name} > {output_pth / 'environment.yml'}"
    )
    command.run(command_string, echo=True)


from invoke import run

env_name = Path(os.environ["CONDA_PREFIX"]).name

output_pth = Path(__file__).parent.parent / "env"

command_string = (
    f"conda env export --name {env_name} --file {output_pth / 'environment.yml'}"
)

result = run(command_string)

print(result)
