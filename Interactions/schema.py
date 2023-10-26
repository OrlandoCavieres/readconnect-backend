from strawberry.tools import merge_types

from Interactions.graphql.queries import BookReviewQuery, BookReviewMutation

InteractionsQueries = merge_types('InteractionsQueries', (BookReviewQuery,))
InteractionsMutations = merge_types('InteractionsMutations', (BookReviewMutation,))
