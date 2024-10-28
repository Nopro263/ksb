import inspect

def Error(description, detail: str = None) -> dict:
    if detail is None:
        detail = description
    
    return {
        "description": description,
        "content": {
            "application/json": {
                "example": {"detail": detail}
            }
        },
    }

def wraps(func):
    def _wraps(replacement):

        sfunc = inspect.signature(func)
        srepl = inspect.signature(replacement)

        def f(*args, **kwargs):
            return replacement(*args, **kwargs)

        sreplp = [p for n,p in srepl.parameters.items() if p.kind != inspect.Parameter.VAR_KEYWORD and p.kind != inspect.Parameter.VAR_POSITIONAL]
        
        smerged = inspect.Signature(
            parameters=[*sfunc.parameters.values(), *sreplp],
            return_annotation=sfunc.return_annotation
        )
    
        f.__signature__ = smerged
        f.__name__ = func.__name__
        f.__doc__ = func.__doc__

        return f
    
    return _wraps