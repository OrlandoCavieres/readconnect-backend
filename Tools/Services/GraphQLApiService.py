from typing import Optional, Any, List, Type

from django.db.models import Model, Q
from numpy import ceil
from strawberry import relay
from strawberry.types import Info

from Schema.Api import Error, PaginationParam, Pagination, Result, Success, ApiMutationAction, ApiQueryAction


class GraphQLApiService:
    """
    Constructs a GraphQLApiService instance.

    :param action: The action to perform.
    :param info: The strawberry.info object.
    :param object_id: The object ID.
    :param filters: The filters for list results.
    :param pagination: The pagination parameters for list results.
    :param order_by: The ordering parameters for list results.
    """
    model: Optional[Type[Model]] = None
    model_verbose: dict[str, str] = {
        'single': 'Modelo',
        'plural': 'Modelos'
    }
    api_object_name = 'Object'
    model_name = 'Model'
    objects_manager = None

    permitted_actions = []
    errors = {
        'invalid': Error(message = 'Acción inválida'),
        'not_impl': Error(message = 'Acción no implementada aún')
    }

    has_special_order = False

    def __init__(self, action: ApiMutationAction | ApiQueryAction, info: Info, object_id: Optional[relay.GlobalID] = None,
                 filters: Optional[Any] = None, pagination: Optional[PaginationParam] = None, order_by: Optional[str] = None,
                 form: Optional[Any] = None):
        self.action = action
        self.info = info
        self.object_id = object_id
        self.filters = filters
        self.pagination = pagination if pagination else PaginationParam()
        self.order_by = order_by if order_by else []
        self.form = form
        self.form_dict = self.form.__dict__ if self.form else None

        self.annotated_query = {}
        self.filter_query = Q()
        self.using_filters = self.filters is not None
        self.query_result = None

        self.cards = []
        self.element = None

    def decide(self):
        """
        Executes a specific action based on the given parameters.

        :return: The result of the action.
        """
        if self.model:
            self.set_objects_manager()

            if self.objects_manager is None:
                return Error(message = f'No se ha establecido correctamente los parámetros del modelo')

            if self.action in [ApiMutationAction.DELETE, ApiMutationAction.UPDATE, ApiQueryAction.VIEW]:
                if self.object_id:
                    self.element = self.get_object_or_none()

                    if not self.element:
                        return Error(message = f'{self.model_verbose['single']} no encontrado')
                else:
                    return Error(message = f'El campo object_id es requerido para la acción {self.action.value.upper()}')

            if self.action in [ApiMutationAction.UPDATE, ApiMutationAction.CREATE]:
                if self.form is None:
                    return Error(message = f'Formulario es requerido para esta acción')

            match self.action:
                case ApiQueryAction.CARD_LIST:
                    self.resolve_query()
                    return self.card_list()

                case ApiMutationAction.CREATE:
                    return self.create()

                case ApiMutationAction.DELETE:
                    return self.delete()

                case ApiQueryAction.LIST:
                    self.resolve_query()
                    return self.list()

                case ApiMutationAction.UPDATE:
                    return self.update()

                case ApiQueryAction.VIEW:
                    return self.view()

                case _:
                    return self.errors['invalid']

    def set_filter_query(self):
        """
        Sets the filter query based on the provided filter parameters.

        :return: None
        """
        pass

    def set_special_order(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def filter_by_global_id(self, field: relay.GlobalID, model_type: Type[Model], query: str):
        """
        Filters the query based on the provided global ID field.

        :param field: The global ID field.
        :param model_type: The type of the model being filtered.
        :param query: The query string to filter on.
        :return: None
        """
        try:
            element = field.resolve_node_sync(info = self.info, ensure_type = model_type)
            self.filter_query &= Q(**{query: [element]})
        except TypeError as e:
            print(e)

    def set_objects_manager(self):
        self.objects_manager = self.model.objects

    def resolve_query(self):
        if self.annotated_query:
            self.query_result = self.objects_manager.annotate(**self.annotated_query)

        self.set_filter_query()

        if self.annotated_query:
            self.query_result = self.query_result.filter(self.filter_query)
        else:
            self.query_result = self.objects_manager.filter(self.filter_query)

        if self.has_special_order:
            self.set_special_order()
        else:
            self.query_result = self.query_result.order_by(self.order_by)

    def card_list(self):
        pass

    def get_object_or_none(self):
        """
        Retrieve an object or return None if it does not exist.

        :return: The object if it exists, otherwise None.
        """
        try:
            return self.object_id.resolve_node_sync(info = self.info, ensure_type = self.model)
        except TypeError:
            return None

    def delete(self):
        """
        Deletes the element.

        :return: Success object indicating that the deletion was successful.
        """
        self.element.delete()
        return Success(message = f'{self.model_verbose['single']} eliminado con éxito',
                       process_name = f'Delete{self.model_name}')

    def list(self):
        pass

    def paginate(self):
        """
        Paginate the query result based on the provided pagination parameters.

        :return: Pagination object with information about the paginated result.
        """
        start, elems = self.pagination.start_position, self.pagination.elements
        total_elements = len(self.query_result)
        total_pages = int(ceil(total_elements / elems))
        actual_page = int(ceil((start + 1) / elems))

        self.query_result = self.query_result[start: start + elems]
        total_consulted = len(self.query_result)
        last = elems * actual_page - 1 if elems * actual_page <= total_elements else start + total_consulted - 1

        return Pagination(
            total_elements = total_elements,
            pages = total_pages,
            consulted_elements = total_consulted,
            actual_page = actual_page,
            page_size = elems,
            first = start,
            last = last
        )

    def view(self):
        """
        View method.

        :return: Result object containing the resolved node.
        """
        return Result(single = self.object_id.resolve_node_sync(info = self.info, ensure_type = self.model))
