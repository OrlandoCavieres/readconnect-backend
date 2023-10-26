from typing import Optional

from strawberry import input, relay

from Schema.Api import TextFilter


@input
class BookFilter(TextFilter):
    category: Optional[relay.GlobalID] = None
    author: Optional[relay.GlobalID] = None
    min_pages_number: Optional[int] = None
    max_pages_number: Optional[int] = None
    min_published_date: Optional[str] = None
    max_published_date: Optional[str] = None
