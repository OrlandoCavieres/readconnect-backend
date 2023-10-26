from strawberry import auto, django, relay

from Users.models import User


@django.type(model = User)
class UserObject(relay.Node):
    id: relay.NodeID[int]
    name: auto
    email: auto
