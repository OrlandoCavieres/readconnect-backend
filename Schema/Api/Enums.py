from enum import Enum
from strawberry import enum


@enum
class ApiMutationAction(Enum):
    CREATE = 'create'
    DELETE = 'delete'
    UPDATE = 'update'


@enum
class ApiQueryAction(Enum):
    CARD_LIST = 'card_list'
    LIST = 'list'
    VIEW = 'view'


@enum
class ApiRelatedAction(Enum):
    ADD = 'add'
    REMOVE = 'remove'


@enum
class UserBookList(Enum):
    WISHED = 'wished'
    FINISHED = 'finished'
