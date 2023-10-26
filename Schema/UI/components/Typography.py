from strawberry import type


@type
class Typography:
    text: str
    color: str = "text"
    size: str = "p1"
    weight: str = "r"
