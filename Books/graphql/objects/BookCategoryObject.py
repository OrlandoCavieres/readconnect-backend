from strawberry import auto, django, relay

from Books.models import BookCategory


@django.type(model = BookCategory)
class BookCategoryObject(relay.Node):
    id: relay.NodeID[int]
    name: auto
