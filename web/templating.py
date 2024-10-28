from fastapi import Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

from utils import wraps

env = Environment(loader=FileSystemLoader("templates"))

class Templated:
    app = None
    def __init__(self, template_name) -> None:
        self.template_name = template_name
    
    @staticmethod
    def static(url: str, file=None):
        if not file:
            file = url.removeprefix("/") + ".html"

        def f():
            template = env.get_template(file)
            output_from_parsed_template = template.render()
            return HTMLResponse(content=output_from_parsed_template)
        
        f.__name__ = file

        f = Templated.app.get(url)(f)
        
        return f
        

    def __call__(self, func):
        @wraps(func)
        def f(*args, request: Request, **kwargs):
            accept = request.headers.get('accept')
            ret_val = func(*args, **kwargs)
            if "text/html" in accept:
                ret_val = self.render(ret_val)
            return ret_val
        
        return f
    
    def render(self, val):
        template = env.get_template(self.template_name)
        output_from_parsed_template = template.render(response=val)
        return HTMLResponse(content=output_from_parsed_template)