from typing import List, Annotated, TYPE_CHECKING


from strawberry import auto, django, field, relay, lazy
from strawberry.types import Info

from Books.graphql.objects import AuthorObject, BookCategoryObject
from Books.models import Book

if TYPE_CHECKING:
    from Interactions.graphql.objects import BookReviewObject


@django.type(model = Book)
class BookObject(relay.Node):
    id: relay.NodeID[int]
    title: auto
    isbn: auto
    page_count: auto

    thumbnail: auto

    short_description: auto
    long_description: auto

    status: auto
    published_date: auto
    published_date_format: auto

    rating: auto
    reviews_number: auto

    @field()
    def authors(self) -> List['AuthorObject']:
        return self.authors.all().order_by('name')

    @field()
    def categories(self) -> List['BookCategoryObject']:
        return self.categories.all().order_by('name')

    @field()
    def reviews(self) -> List[Annotated["BookReviewObject", lazy("Interactions.graphql.objects")]]:
        return self.reviews.all().order_by('-last_update')

    @field()
    def in_wish_list(self, info: Info) -> bool:
        return self.in_user_wished_list(info.context.request.user)

    @field()
    def in_finished_list(self, info: Info) -> bool:
        return self.in_user_finished_list(info.context.request.user)
