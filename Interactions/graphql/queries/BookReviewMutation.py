from typing import Optional

from strawberry import field, type, relay
from strawberry.types import Info

from Interactions.graphql.forms import BookReviewForm
from Interactions.graphql.responses import BookReviewMutationResponse
from Interactions.services import BookReviewService
from Schema.Api import ApiMutationAction
from Schema.Permissions import IsAuthenticated


@type
class BookReviewMutation:
    @field(permission_classes = [IsAuthenticated])
    def books_reviews(self, info: Info,
                      action: ApiMutationAction,
                      form: Optional[BookReviewForm] = None,
                      object_id: Optional[relay.GlobalID] = None) -> BookReviewMutationResponse:
        service = BookReviewService(action = action, info = info, object_id = object_id, form = form)
        result = service.decide()
        return result
