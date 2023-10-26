from typing import Optional

from strawberry import input


@input
class PaginationParam:
    elements: Optional[int] = 50
    start_position: Optional[int] = 0


@input
class TextFilter:
    text: Optional[str] = None
