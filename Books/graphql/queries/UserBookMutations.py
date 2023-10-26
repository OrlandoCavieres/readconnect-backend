from strawberry import mutation, type, relay
from strawberry.types import Info

from Books.graphql.responses import BookListActionResponse
from Books.models import Book
from Schema.Api import Error, NoChanges, Success
from Schema.Api.Enums import UserBookList, ApiRelatedAction
from Schema.Permissions import IsAuthenticated


@type
class UserBookMutations:
    @mutation(permission_classes = [IsAuthenticated])
    def user_book_list(self, info: Info, action: ApiRelatedAction,
                       list_target: UserBookList, book_id: relay.GlobalID) -> BookListActionResponse:
        user = info.context.request.user

        try:
            book = book_id.resolve_node_sync(info = info, ensure_type = Book)
            in_wish = book.in_user_wished_list(user)
            in_finished = book.in_user_finished_list(user)

            if list_target == UserBookList.WISHED:
                if action == ApiRelatedAction.ADD:
                    if in_wish:
                        return NoChanges()
                    elif in_finished:
                        user.books_finished.remove(book)

                    user.books_wish_list.add(book)

                elif action == ApiRelatedAction.REMOVE:
                    if in_wish:
                        user.books_wish_list.remove(book)
                    else:
                        return Error(message = 'Libro no se encuentra en lista por leer')

            elif list_target == UserBookList.FINISHED:
                if action == ApiRelatedAction.ADD:
                    if in_finished:
                        return NoChanges()
                    elif in_wish:
                        user.books_wish_list.remove(book)

                    user.books_finished.add(book)

                elif action == ApiRelatedAction.REMOVE:
                    if in_finished:
                        user.books_finished.remove(book)
                    else:
                        return Error(message = 'Libro no se encuentra en la lista de leídos')

            return Success(message = f"Libro {'removido' if action == ApiRelatedAction.REMOVE else 'agregado'} exitosamente a lista "
                                     f"{'por leer' if list_target == UserBookList.WISHED else 'de leídos'}")

        except TypeError:
            return Error(message = 'Libro no encontrado')
