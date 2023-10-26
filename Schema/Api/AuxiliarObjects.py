from strawberry import type


@type
class Pagination:
    pages: int
    actual_page: int
    page_size: int
    total_elements: int
    consulted_elements: int
    first: int
    last: int
