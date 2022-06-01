import os

import typer
from click.testing import CliRunner
from pathlib import Path

import black as black_module
from mypy import api as mypy_api

import subprocess
import invoke

app = typer.Typer()

code_root = output_pth = Path(__file__).parent
context = invoke.Context()


@app.command()
def black():
    runner = CliRunner()

    result = runner.invoke(black_module.main, [str(code_root / 'src')])

    assert result.exit_code == 0
    print(result.output)


@app.command()
def mypy():

    result = mypy_api.run(['.'])
    if result[0]:
        print(result[0])

@app.command()
def export_env(
               filename: str = 'environment.yml',
               override_channels: bool = False,
               no_builds: bool = False,
               ignore_channels: bool = False,
               from_history: bool = False):

    env_name = Path(os.environ["CONDA_PREFIX"]).name

    print(env_name)

    output_pth = Path(__file__).parent / "env"
    print(__file__)
    print(output_pth)

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

    #subprocess.call(args)



if __name__ == "__main__":
    #args = ['conda']#, 'env', 'export', '--name', 'py39_main']
    #subprocess.call(args)

    app()