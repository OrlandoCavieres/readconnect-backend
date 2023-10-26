from datetime import datetime
from typing import Optional, List

import rich
from django.db.models import Q, Subquery, OuterRef
from django.db.models.functions import Concat
from strawberry import relay
from strawberry.scalars import Base64
from strawberry.types import Info

from Books.graphql.filters import BookFilter
from Books.models import Book, Author, BookCategory
from Schema.Api import ApiMutationAction, ApiQueryAction, PaginationParam, Empty, Result
from Schema.Api.Enums import UserBookList
from Schema.UI.components import Card, Container, BookCategoryTag, BackgroundImage, Title, Description
from Tools.Services.GraphQLApiService import GraphQLApiService


class BookService(GraphQLApiService):
    def __init__(self, action: ApiMutationAction | ApiQueryAction,
                 info: Info,
                 user_list: Optional[UserBookList] = None,
                 object_id: Optional[relay.GlobalID] = None,
                 filters: Optional[BookFilter] = None,
                 pagination: Optional[PaginationParam] = None,
                 order_by: Optional[str] = None):
        super().__init__(action = action, info = info, object_id = object_id, filters = filters,
                         pagination = pagination, order_by = order_by)
        self.model = Book
        self.model_verbose['single'] = 'Libro'
        self.model_verbose['plural'] = 'Libros'
        self.model_name = 'Book'
        self.api_object_name = 'BookObject'

        self.user_list = user_list
        self.has_special_order = 'authors' in order_by or 'categories' in order_by or 'rating' in order_by

    def set_filter_query(self):
        if self.filters:
            # Text filter for book title
            if self.filters.text:
                parts = [s for s in self.filters.text.strip().split(' ') if s]

                for p in parts:
                    self.filter_query &= Q(title__icontains = p)

            # Filter books by author, using a GlobalID from relay
            if self.filters.author:
                self.filter_by_global_id(self.filters.author, Author, 'authors__in')

            # Filter books by category, using a GlobalID from relay
            if self.filters.category:
                self.filter_by_global_id(self.filters.category, BookCategory, 'categories__in')

            # Filter books by a minimum number of pages
            if self.filters.min_pages_number is not None:
                self.filter_query &= Q(page_count__gte = self.filters.min_pages_number)

            # Filter books by a maximum number of pages
            if self.filters.max_pages_number is not None:
                self.filter_query &= Q(page_count__lte = self.filters.max_pages_number)

            # Filter books by a minimum published date
            if self.filters.min_published_date is not None:
                self.filter_query &= Q(published_date__date__gte = self.filters.min_published_date)

            # Filter books by a maximum published date
            if self.filters.max_published_date is not None:
                self.filter_query &= Q(published_date__date__lte = self.filters.max_published_date)

    def set_special_order(self):
        if 'authors' in self.order_by:
            self.query_result = sorted(self.query_result, key = lambda e: e.authors_str_ordered, reverse = '-' in self.order_by)

        elif 'categories' in self.order_by:
            self.query_result = sorted(self.query_result, key = lambda e: e.categories_str_ordered, reverse = '-' in self.order_by)

        elif 'rating' in self.order_by:
            self.query_result = sorted(self.query_result, key = lambda e: e.rating, reverse = '-' in self.order_by)

    def set_objects_manager(self):
        if self.user_list:
            if self.user_list == UserBookList.WISHED:
                self.objects_manager = self.info.context.request.user.books_wish_list

            elif self.user_list == UserBookList.FINISHED:
                self.objects_manager = self.info.context.request.user.books_finished
        else:
            self.objects_manager = self.model.objects

    def card_list(self):
        pagination_response = self.paginate()

        if pagination_response.consulted_elements == 0 or pagination_response.total_elements == 0:
            return Empty()

        cards = []

        for book in self.query_result:
            authors = ' - '.join([author.name for author in book.authors.all().order_by('name')])

            sections = [
                BackgroundImage(
                    url = book.thumbnail,
                    alt_text = f'Imagen de la portada del libro {book.title} usada como fondo de la tarjeta'
                ),
                Container(
                    elements = [
                        Title(text = book.title, color = 'secondary'),
                        Description(text = f"Por {authors}" if authors else 'Autor desconocido', color = 'terciary', size = 'h6')
                    ]
                ),
                Container(
                    elements = [
                        Description(
                            text = (book.short_description if len(book.short_description) <= 160 else f'{book.short_description[:161]}...')
                            if book.short_description else 'Sin descripción'),
                        Description(
                            color = 'textDecorate',
                            text = f'Publicado el {datetime.strftime(book.published_date, "%d/%m/%Y")}'
                            if book.published_date else 'Sin fecha de publicación'
                        )
                    ]
                ),
                Container(
                    justify = 'flex-start',
                    align = 'center',
                    direction = 'row',
                    elements = [BookCategoryTag(name = category.name) for category in book.categories.all().order_by('name')]
                )
            ]

            relay_id = f'{self.api_object_name}:{book.id}'
            cards.append(Card(
                id = Base64(relay_id.encode()),
                in_wish_list = book.in_user_wished_list(self.info.context.request.user),
                in_finished_list = book.in_user_finished_list(self.info.context.request.user),
                sections = sections)
            )

        return Result(message = 'Lista de tarjetas obtenida con éxito', cards = cards,
                      pagination=pagination_response, using_filters = self.using_filters)

    def list(self):
        pagination_response = self.paginate()

        if pagination_response.consulted_elements == 0 or pagination_response.total_elements == 0:
            return Empty()

        return Result(message = 'Lista obtenida con éxito', list = self.query_result,
                      pagination = pagination_response, using_filters = self.using_filters)

    def create(self):
        return self.errors['not_impl']

    def update(self):
        return self.errors['not_impl']
