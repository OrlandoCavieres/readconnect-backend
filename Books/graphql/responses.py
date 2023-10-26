from typing import List

from strawberry import type, union

from Books.graphql.objects import BookObject, AuthorObject, BookCategoryObject
from Schema.Api import Result, Empty, Error, Success, NoChanges


@type
class BookFilterValuesResponse:
    authors: List['AuthorObject']
    categories: List['BookCategoryObject']


BookQueryResponse = union('BookQueryResponse', (Result[BookObject], Empty, Error))
BookListActionResponse = union('BookListActionResponse', (Success, NoChanges, Error))
