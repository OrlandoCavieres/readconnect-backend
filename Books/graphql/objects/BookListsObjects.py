from strawberry import auto, django, relay, type

from Books.graphql.objects import BookObject
from Books.models import FinishedBook, WishReadBook
from Users.graphql.objects.UserObject import UserObject


@type
class BookListObject:
    user: UserObject
    book: BookObject
    added_on: auto
    removed_on: auto


@django.type(model = FinishedBook)
class FinishedBookObject(relay.Node, BookListObject):
    id: relay.NodeID[int]


@django.type(model = WishReadBook)
class WishReadBookObject(relay.Node, BookListObject):
    id: relay.NodeID[int]
