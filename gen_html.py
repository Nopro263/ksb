from jinja2 import Environment, FileSystemLoader
import os
import sys
import shutil
import re
from watchfiles import watch

html = os.path.join("nginx", "html")
templates = os.path.join('nginx', 'templates')
langs = os.path.join("lang")

env = Environment(loader=FileSystemLoader(templates))


def main():
    for h in os.listdir(html):
        if os.path.isdir(os.path.join(html, h)):
            shutil.rmtree(os.path.join(html, h))
        else:
            os.remove(os.path.join(html, h))
    
    for lang in os.listdir(langs):
        _main(translations={"home": lang}, html=os.path.join(html, lang))

def _main(translations={}, html=html):
    if os.path.exists(html) and os.path.isdir(html):
        for file in os.listdir(html):
            os.remove(os.path.join(html, file))
    else:
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

                for key, value in translations.items():
                    output_from_parsed_template = output_from_parsed_template.replace(f"%{key}%", value)

                with open(os.path.join(html, file), "w") as fh:
                    fh.write(output_from_parsed_template)
                continue
        
        with open(os.path.join(html, file), "wb") as fh:
                with open(os.path.join(templates, file), "rb") as f:
                    fh.write(f.read())

if len(sys.argv) >= 2 and sys.argv[1] == "watch":
    for changes in watch(templates, raise_interrupt=False):
        print("Reloading templates")
        main()
elif len(sys.argv) >= 2 and sys.argv[1] == "generate":
    translations = []
    for file in os.listdir(templates):
        o, ext = os.path.splitext(file)
        _, ext2 = os.path.splitext(o)
        match ext:
            case ".html":
                if ext2 == ".jinja2":
                    continue
                
                template = env.get_template(file)
                output_from_parsed_template = template.render()

                ms = re.findall(r"%(.*?)%", output_from_parsed_template)
                for m in ms:
                    if m not in translations:
                        translations.append(m)
                continue
    
    lang = input("Name of language (eg. de): ")
    if not os.path.exists(langs):
        os.mkdir(langs)
    
    lang = os.path.join(langs, lang)

    with open(lang, "w") as f:
        for translation in translations:
            f.write(f"{translation}:    \n")
else:
    main()