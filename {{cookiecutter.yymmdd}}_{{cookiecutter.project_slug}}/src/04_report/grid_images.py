# %%

from hal.report import Markdown
from hal.config import cfg

# %%

images = ["dog", "cat", "mouse", "bird"]
md_file = Markdown(cfg.paths.output / "04_report" / "my_images.md")
for img in images:
    md_file.heading(f"Image of a: {img}", 2)
    md_file.line()
    md_file.image(f"../03_view/animals/{img}.png", img)
    md_file.line()
    md_file.line()

md_file.write()
