from typing import Optional, List, TypeVar, Generic

from strawberry import type

from Schema.Api import Pagination
from Schema.UI.components import Card


T = TypeVar('T')


@type
class Message:
    message: Optional[str] = 'Sin mensaje'


@type
class Empty(Message):
    message: Optional[str] = 'Sin resultados'


@type
class NoChanges(Message):
    message: Optional[str] = 'No hay cambios'


@type
class Success(Message):
    process_name: Optional[str] = None
    fields_number: Optional[int] = 0
    fields_changed_names: Optional[List[str]] = None


@type
class Result(Generic[T], Message):
    single: Optional[T] = None
    list: Optional[List[T]] = None
    cards: Optional[List[Card]] = None
    pagination: Optional[Pagination] = None
    using_filters: Optional[bool] = False


@type
class FieldErrors:
    field: str
    errors: List[str]


@type
class Error(Message):
    fields: Optional[List[FieldErrors]] = None
