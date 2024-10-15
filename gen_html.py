from jinja2 import Environment, FileSystemLoader
import os
import shutil

html = os.path.join("nginx", "html")
templates = os.path.join('nginx', 'templates')

env = Environment(loader=FileSystemLoader(templates))

if os.path.exists(html) and os.path.isdir(html):
    shutil.rmtree(html)
os.mkdir(html)

for file in os.listdir(templates):
    o, ext = os.path.splitext(file)
    _, ext2 = os.path.splitext(o)
    match ext:
        case ".html":
            if ext2 == ".jinja2":
                 continue
            
            template = env.get_template(file)
            output_from_parsed_template = template.render()

            with open(os.path.join(html, file), "w") as fh:
                fh.write(output_from_parsed_template)
            continue
    
    with open(os.path.join(html, file), "wb") as fh:
            with open(os.path.join(templates, file), "rb") as f:
                fh.write(f.read())