from strawberry import Schema
from strawberry.tools import merge_types

from Books.schema import BookQueries, BookMutations
from Interactions.schema import InteractionsQueries, InteractionsMutations
from Users.schema import UsersMutations, UsersQueries


AllMutations = merge_types('AllMutations', (UsersMutations, BookMutations, InteractionsMutations))
AllQueries = merge_types('AllQueries', (BookQueries, InteractionsQueries, UsersQueries))


schema = Schema(query = AllQueries, mutation = AllMutations)
