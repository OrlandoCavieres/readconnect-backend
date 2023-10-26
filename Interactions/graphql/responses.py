from strawberry import union

from Interactions.graphql.objects import BookReviewObject
from Schema.Api import Result, Empty, Error, Success


BookReviewQueryResponse = union('BookReviewQueryResponse', (Result[BookReviewObject], Empty, Error))
BookReviewMutationResponse = union('BookReviewMutationResponse', (Success, Error))
