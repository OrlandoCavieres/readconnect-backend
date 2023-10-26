from typing import Optional, TYPE_CHECKING, Annotated

from strawberry import auto, django, relay, lazy, field
from strawberry.types import Info

from Interactions.models import BookReview
from Users.graphql.objects.UserObject import UserObject

if TYPE_CHECKING:
    from Books.graphql.objects import BookObject


@django.type(model = BookReview)
class BookReviewObject(relay.Node):
    id: relay.NodeID[int]
    user: Optional['UserObject'] = None
    book: Optional[Annotated["BookObject", lazy("Books.graphql.objects")]] = None
    body: auto
    rating: auto
    last_update: auto
    last_update_format: auto

    @field()
    def from_logged_user(self, info: Info) -> bool:
        return self.created_by_logged_user(info.context.request.user)
