from pathlib import Path


def longpath(pth: Path) -> Path:
    """Converts input `pth` to long path compatible format"""
    return Path(r"//?/" + str(pth))
