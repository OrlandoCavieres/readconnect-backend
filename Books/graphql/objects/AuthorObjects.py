from strawberry import auto, django, relay

from Books.models import Author


@django.type(model = Author)
class AuthorObject(relay.Node):
    id: relay.NodeID[int]
    name: auto
