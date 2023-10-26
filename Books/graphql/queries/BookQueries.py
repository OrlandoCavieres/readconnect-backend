from typing import Optional

from strawberry import field, type, relay
from strawberry.types import Info

from Books.graphql.filters import BookFilter
from Books.graphql.responses import BookQueryResponse, BookFilterValuesResponse
from Books.models import Author, BookCategory
from Books.services import BookService
from Schema.Api import ApiQueryAction, PaginationParam
from Schema.Api.Enums import UserBookList
from Schema.Permissions import IsAuthenticated


@type
class BookQuery:
    @field(permission_classes = [IsAuthenticated])
    def books(self, info: Info,
              action: Optional[ApiQueryAction] = ApiQueryAction.LIST,
              user_list: Optional[UserBookList] = None,
              object_id: Optional[relay.GlobalID] = None,
              filters: Optional[BookFilter] = None,
              pagination: Optional[PaginationParam] = None,
              order_by: Optional[str] = None) -> BookQueryResponse:
        if order_by is None:
            order_by = 'title'

        service = BookService(action = action, info = info, user_list = user_list, object_id = object_id, filters = filters,
                              pagination = pagination, order_by = order_by)
        result = service.decide()
        return result

    @field(permission_classes = [IsAuthenticated])
    def book_filters_values(self, info: Info) -> BookFilterValuesResponse:
        authors = Author.objects.all().order_by('name')
        categories = BookCategory.objects.all().order_by('name')
        return BookFilterValuesResponse(authors = authors, categories = categories)
