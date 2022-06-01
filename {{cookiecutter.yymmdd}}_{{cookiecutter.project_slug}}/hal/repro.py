import sys
from types import ModuleType
from typing import Union, Generator, Optional, Iterable
import watermark
import shutil
import click
from pathlib import Path
from datetime import datetime
import distutils.sysconfig as sysconfig
from hal.config import cfg
import os


def gen_imports(globals_: dict) -> Generator:
    for name, val in globals_.items():
        if isinstance(val, ModuleType):
            base_module = val.__name__.split(".")[0]
            yield base_module
        else:
            try:
                yield val.__module__.split(".")[0]
            except AttributeError:
                pass


def reproduce(
    script_path: Path,
    output_path: Path,
    globals_: dict,
    packages: Optional[Iterable[str]] = None,
    **watermark_kwargs,
) -> None:

    rpr_path = output_path / "_rpr"
    rpr_path.mkdir(exist_ok=True, parents=True)

    script_target = rpr_path / script_path.name

    py_files = list(rpr_path.glob("*.py"))
    if len(py_files) >= 2:
        raise ValueError(
            f"Reproducibility directory should only have 1 .py file, got {len(py_files)}"
        )
    elif len(py_files) == 1 and py_files[0].name != script_path.name:
        text = f"Override existing result from script {py_files[0].name!r}?"
        confirm = click.confirm(text, default=False)
        if not confirm:
            return

    # Copy source script
    shutil.copy(script_path, script_target)

    # Copy scripts in toolbox
    tools_pth = rpr_path / "toolbox"
    tools_pth.mkdir(exist_ok=True, parents=True)
    for script in (cfg.paths.src / "toolbox").glob("*.py"):
        shutil.copy(script, tools_pth / script.name)

    combined = set(packages or []) | set(gen_imports(globals_))

    # Remove builtins
    combined -= {sys.builtin_module_names}

    # Remove standard library
    stdlib_pth = sysconfig.get_python_lib(standard_lib=True)
    stdlib = {p.stem.replace(".py", "") for p in Path(stdlib_pth).iterdir()}
    combined -= stdlib

    packages = ",".join(sorted(combined))
    dave_kwargs = dict(
        author="Jochem H. Smit",
        current_time=True,
        current_date=True,
        timezone=True,
        updated=True,
        python=True,
        conda=True,
        githash=True,
        machine=True,
    )

    dave_kwargs.update(watermark_kwargs)
    dave = watermark.watermark(globals_=globals_, packages=packages, **dave_kwargs)

    (rpr_path / "watermark.txt").write_text(dave)
