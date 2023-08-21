from contextlib import contextmanager
from pathlib import Path


class Markdown:
    def __init__(self, file_path: Path, content: str = "") -> None:
        self.file_path = file_path
        self.content = content

    @contextmanager
    def tab_set(self):
        self.content += "````{tab-set}\n"
        try:
            yield None
        finally:
            self.content += "````\n"

    @contextmanager
    def tab_item(self, title):
        self.content += f"```{{tab-item}} {title}\n"
        try:
            yield None
        finally:
            self.content += "```\n"

    def line(self, line: str = "") -> None:
        self.content += line + "\n"

    def image(self, path: str, alt_text: str) -> None:
        self.content += f"![{alt_text}]({path})\n"

    def heading(self, text: str, level: int) -> None:
        self.content += "#" * level + " " + text + "\n"

    def write(self):
        self.file_path.write_text(self.content)
