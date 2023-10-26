from typing import Optional

import rich
from django.forms import ModelForm
from strawberry import relay
from strawberry.types import Info

from Books.models import Book
from Interactions.graphql.forms import BookReviewForm
from Interactions.models import BookReview
from Schema.Api import ApiMutationAction, ApiQueryAction, PaginationParam, Empty, Result, Error, FieldErrors, Success
from Tools.Services.GraphQLApiService import GraphQLApiService


class BookReviewModelForm(ModelForm):
    class Meta:
        model = BookReview
        fields = ['book', 'body', 'rating', 'user']


class BookReviewService(GraphQLApiService):
    def __init__(self, action: ApiMutationAction | ApiQueryAction,
                 info: Info,
                 book_id: Optional[relay.GlobalID] = None,
                 object_id: Optional[relay.GlobalID] = None,
                 filters = None,
                 pagination: Optional[PaginationParam] = None,
                 order_by: Optional[str] = None,
                 form: Optional[BookReviewForm] = None):
        super().__init__(action = action, info = info, object_id = object_id, filters = filters,
                         pagination = pagination, order_by = order_by, form = form)
        self.model = BookReview
        self.model_verbose['single'] = 'Comentario'
        self.model_verbose['plural'] = 'Comentarios'
        self.model_name = 'BookReview'
        self.api_object_name = 'BookReviewObject'

        self.book_id = book_id

    def set_objects_manager(self):
        if self.book_id:
            try:
                book = self.book_id.resolve_node_sync(info = self.info, ensure_type = Book)
                self.objects_manager = book.reviews

            except TypeError:
                self.objects_manager = None

        else:
            self.objects_manager = self.model.objects

    def list(self):
        pagination_response = self.paginate()

        if pagination_response.consulted_elements == 0 or pagination_response.total_elements == 0:
            return Empty()

        return Result(message = 'Lista obtenida con éxito', list = self.query_result,
                      pagination = pagination_response, using_filters = self.using_filters)

    def create(self):
        model_form = BookReviewModelForm()

        try:
            if self.form.book:
                book = self.form.book.resolve_node_sync(info = self.info, ensure_type = Book)

                self.form_dict['book'] = book.id
                self.form_dict['user'] = self.info.context.request.user
                model_form.data = self.form_dict
                model_form.is_bound = True
                model_form.is_valid()

                errors = []

                if model_form.errors:
                    errors = [FieldErrors(field = k, errors = v) for k, v in model_form.errors.items()]

                if errors:
                    return Error(message = 'Errores presentes en el formulario de creación', fields = errors)

                model_form.save()
                return Success(message = 'Comentario creado con éxito', process_name = 'BookReviewCreate')

        except TypeError:
            return Error(message = 'Debe suministrarse en el formualrio el ID de libro a asociar')

    def update(self):
        model_form = BookReviewModelForm(instance = self.object_id.resolve_node_sync(info = self.info, ensure_type = BookReview))

        model_form.data = {**model_form.initial, **{k: v for k, v in self.form_dict.items() if v is not None}}
        model_form.is_bound = True
        model_form.is_valid()

        errors = []

        if model_form.errors:
            errors = [FieldErrors(field = k, errors = v) for k, v in model_form.errors.items()]

        if errors:
            return Error(message = 'Errores presentes en el formulario de creación', fields = errors)

        model_form.save()
        return Success(message = 'Comentario actualizado con éxito', process_name = 'BookReviewUpdate')

