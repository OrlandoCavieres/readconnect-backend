from strawberry import Schema, type, field
from strawberry.tools import merge_types

from Books.schema import BookQueries, BookMutations
from Interactions.schema import InteractionsQueries, InteractionsMutations
from Schema.Permissions import IsAuthenticated
from Users.schema import UsersMutations, UsersQueries


@type
class Query:
    @field()
    def hola(self) -> str:
        return 'Hola mundo'

    @field(permission_classes = [IsAuthenticated])
    def prohibido(self) -> str:
        return 'Prohibido'


AllMutations = merge_types('AllMutations', (UsersMutations, BookMutations, InteractionsMutations))
AllQueries = merge_types('AllQueries', (Query, BookQueries, InteractionsQueries, UsersQueries))


schema = Schema(query = AllQueries, mutation = AllMutations)
