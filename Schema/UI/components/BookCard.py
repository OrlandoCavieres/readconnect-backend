from typing import Optional, List

from strawberry import type, union
from strawberry.scalars import Base64

from Schema.UI.components.Typography import Typography


@type
class BackgroundImage:
    url: str
    alt_text: Optional[str] = 'Imagen de fondo'


@type
class BookCategoryTag:
    name: str


@type
class Title(Typography):
    size: str = 'h5'
    weight: str = 'b'


@type
class Description(Typography):
    pass


@type
class AbsoluteContainer:
    top: int = 0
    bottom: int = 0
    left: int = 0
    right: int = 0
    direction: str = 'column'
    gap: int = 10
    elements: List['InnerElement']


@type
class Container:
    justify: str = 'none'
    align: str = 'none'
    direction: str = 'column'
    gap: int = 5
    elements: List['InnerElement']


InnerElement = union('InnerElement', (BookCategoryTag, Title, Description))
CardSection = union('CardSection', (BackgroundImage, Title, Description, Container, AbsoluteContainer))


@type
class Card:
    id: Base64
    in_wish_list: bool = False
    in_finished_list: bool = False
    sections: List[CardSection]
