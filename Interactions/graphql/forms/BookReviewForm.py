from typing import Optional

from strawberry import input, relay


@input
class BookReviewForm:
    book: Optional[relay.GlobalID] = None
    body: Optional[str] = None
    rating: Optional[int] = None
