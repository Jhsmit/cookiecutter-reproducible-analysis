import distutils.sysconfig as sysconfig
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Generator, Iterable, Optional
import zipfile

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
    relpath = script_path.relative_to(cfg.paths.src)
    output_path = cfg.paths.output / relpath.parent / relpath.stem
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
        author="{{cookiecutter.author_name}}",
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

    with zipfile.ZipFile(
        output_path / "_rpr.zip", "w", zipfile.ZIP_DEFLATED
    ) as rpr_zip:
        rpr_zip.write(script_path, script_path.name)
        rpr_zip.writestr("watermark.txt", dave)

        toolbox_dir = cfg.paths.src / "toolbox"
        if toolbox_dir.exists():
            zipdir(toolbox_dir, rpr_zip)

    return output_path


def reproduce(
    globals_: dict,
    packages: Optional[Iterable[str]] = None,
    **watermark_kwargs,
) -> Path:
    script_path = Path(globals_["__file__"])
    relpath = script_path.relative_to(cfg.paths.src)
    output_path = cfg.paths.output / relpath.parent / relpath.stem

    rpr_path = output_path / "_rpr"
    rpr_path.mkdir(exist_ok=True, parents=True)
    script_target = rpr_path / script_path.name

    py_files = list(rpr_path.glob("*.py"))
    if len(py_files) >= 2:
        raise ValueError(
            f"Reproducibility directory should only have 1 .py file, got {len(py_files)}"
        )

    # Copy source script
    shutil.copy(script_path, script_target)

    # Copy scripts in toolbox
    tools_pth = rpr_path / "toolbox"
    tools_pth.mkdir(exist_ok=True, parents=True)
    for script in (cfg.paths.src / "toolbox").glob("*.py"):
        shutil.copy(script, tools_pth / script.name)

    combined = set(packages or []) | set(gen_imports(globals_)) | set(cfg.packages)

    # Remove builtins
    combined -= {sys.builtin_module_names}

    # Remove standard library
    stdlib_pth = sysconfig.get_python_lib(standard_lib=True)
    stdlib = {p.stem.replace(".py", "") for p in Path(stdlib_pth).iterdir()}
    combined -= stdlib

    # Remove hal
    combined -= {"hal"}

    packages = ",".join(sorted(combined))
    dave_kwargs = dict(
        author="{{cookiecutter.author_name}}",
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

    return output_path
