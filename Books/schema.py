from strawberry.tools import merge_types

from Books.graphql.queries import BookQuery, UserBookMutations

BookQueries = merge_types('BookQueries', (BookQuery,))
BookMutations = merge_types('BookMutations', (UserBookMutations,))
