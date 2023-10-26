from typing import Optional

from strawberry import field, type, relay
from strawberry.types import Info

from Interactions.graphql.responses import BookReviewQueryResponse
from Interactions.services import BookReviewService
from Schema.Api import ApiQueryAction, PaginationParam
from Schema.Permissions import IsAuthenticated


@type
class BookReviewQuery:
    @field(permission_classes = [IsAuthenticated])
    def books_reviews_list(self, info: Info,
                           book_id: Optional[relay.GlobalID] = None,
                           pagination: Optional[PaginationParam] = None) -> BookReviewQueryResponse:
        order_by = '-last_update'

        service = BookReviewService(action = ApiQueryAction.LIST, info = info, book_id = book_id,
                                    pagination = pagination, order_by = order_by)
        result = service.decide()
        return result
