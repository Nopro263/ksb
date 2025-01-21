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
    
    translate()
    
    for lang in os.listdir(langs):
        _main(translations=parse_translations(os.path.join(langs, lang)), html=os.path.join(html, lang))

def parse_translations(path: str) -> dict:
    translations = {}
    with open(path, "r") as f:
        for line in f.readlines():
            s = line.split(":    ")
            translations[s[0]] = s[1].strip().replace("\\n", "\n")
    
    return translations

def write_translations(path: str, translations: dict):
    if isinstance(translations, list):
        translations = {key:"" for key in translations}

    with open(path, "w") as f:
        for key, value in translations.items():
            f.write(f"{key}:    {value}\n")

def translate():
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
        
        with open(os.path.join(templates, file), "rb") as f:
            d = f.read()
            ms = re.findall(r"%(.*?)%".encode("utf-8"), d)
            for m in ms:
                if m not in translations:
                    translations.append(m.decode("utf-8"))
            continue
    
    for l in os.listdir(langs):
        lang = os.path.join(langs, l)

        data = parse_translations(lang)
        for translation in translations:
            if translation not in data:
                data[translation] = ""
        
        for key in data.keys():
            if key not in translations:
                del data[key]
        
        write_translations(lang, data)

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
                    d = f.read()
                    for key, value in translations.items():
                        d = d.replace(f"%{key}%".encode("utf-8"), value.encode("utf-8"))
                    fh.write(d)

if len(sys.argv) >= 2 and sys.argv[1] == "watch":
    self_changed = False
    for changes in watch(templates, langs, raise_interrupt=False):
        if self_changed:
            self_changed = False
            continue
        print("Reloading templates")
        if not self_changed:
            main()
            self_changed = True
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
        
        with open(os.path.join(templates, file), "rb") as f:
            d = f.read()
            ms = re.findall(r"%(.*?)%".encode("utf-8"), d)
            for m in ms:
                if m not in translations:
                    translations.append(m.decode("utf-8"))
            continue
    
    lang = input("Name of language (eg. de ENTER to append to all): ")
    if lang:
        if not os.path.exists(langs):
            os.mkdir(langs)
        
        lang = os.path.join(langs, lang)

        write_translations(lang, translations)
    else:
        for l in os.listdir(langs):
            lang = os.path.join(langs, l)

            data = parse_translations(lang)
            for translation in translations:
                if translation not in data:
                    data[translation] = ""
            
            for key in data.keys():
                if key not in translations:
                    del data[key]
            
            write_translations(lang, data)
else:
    main()