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