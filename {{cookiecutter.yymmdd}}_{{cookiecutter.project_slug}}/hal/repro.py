import distutils.sysconfig as sysconfig
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from types import ModuleType
from typing import Generator, Iterable, Optional

import watermark

from hal.config import cfg


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


def zipdir(path: Path, zipf: zipfile.ZipFile):
    for file_path in path.glob("**/*"):
        if "__pycache__" in file_path.parts:
            continue

        if file_path.is_file():
            zipf.write(file_path, file_path.relative_to(path.parent))


def reproduce(
    globals_: dict,
    packages: Optional[Iterable[str]] = None,
    **watermark_kwargs,
) -> Path:
    script_path = Path(globals_["__file__"])
    relpath = script_path.relative_to(cfg.root / "ava")
    output_path = cfg.root / "output" / relpath.parent / relpath.stem
    output_path.mkdir(exist_ok=True, parents=True)

    combined = set(packages or []) | set(gen_imports(globals_))

    # Remove builtins
    combined -= {sys.builtin_module_names}

    # Remove standard library
    stdlib_pth = sysconfig.get_python_lib(standard_lib=True)
    stdlib = {p.stem.replace(".py", "") for p in Path(stdlib_pth).iterdir()}
    combined -= stdlib

    # Remove hal
    combined -= {"hal", "builtins", "src"}

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

    # Run the command and capture the output
    freeze = subprocess.run(["uv", "pip", "freeze"], capture_output=True, text=True)

    # write to root freeze.txt file
    if not freeze.stderr:
        freeze_file = cfg.root / "freeze.txt"
        with open(freeze_file, "w") as f:
            f.write("# uv pip freeze output generated at ")
            f.write(datetime.now().isoformat())
            f.write("\n")
            f.write(freeze.stdout)

    with zipfile.ZipFile(
        output_path / "_rpr.zip", "w", zipfile.ZIP_DEFLATED
    ) as rpr_zip:
        rpr_zip.write(script_path, script_path.name)
        rpr_zip.writestr("watermark.txt", dave)

        rpr_zip.writestr("pip_freeze.txt", freeze.stdout)
        if freeze.stderr:
            rpr_zip.writestr("pip_freeze_error.txt", freeze.stderr)

        toolbox_dir = cfg.root / "ava" / "toolbox"
        if toolbox_dir.exists():
            zipdir(toolbox_dir, rpr_zip)

    return output_path
