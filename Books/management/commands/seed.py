import json

from django.core.management import BaseCommand
from oauth2_provider.models import Application, AbstractApplication

from Books.models import Author, BookCategory, Book
from ReadConnect.settings import BASE_DIR
from Users.models import User


class Command(BaseCommand):
    help = 'Seed database with initial books data'

    def handle(self, *args, **kwargs):
        with open(f'{BASE_DIR}/amazon.book.json') as json_file:
            json_data = json.load(json_file)

            for book in json_data:
                authors = []
                categories = []

                if 'authors' in book:
                    for author in book['authors']:
                        if author:
                            bd_author = Author.objects.filter(name = author).first()

                            if bd_author:
                                authors.append(bd_author)

                            else:
                                new_author = Author(name = author)
                                new_author.save()
                                authors.append(new_author)

                if 'categories' in book:
                    for category in book['categories']:
                        if category:
                            bd_category = BookCategory.objects.filter(name = category).first()

                            if bd_category:
                                categories.append(bd_category)

                            else:
                                new_category = BookCategory(name = category)
                                new_category.save()
                                categories.append(new_category)

                new_book = Book(
                    title = book['title'],
                    isbn = book['isbn'] if 'isbn' in book else '',
                    page_count = book['pageCount'],
                    short_description = book['shortDescription'] if 'shortDescription' in book else '',
                    long_description = book['longDescription'] if 'longDescription' in book else '',
                    status = book['status'] if 'status' in book else 'UNKNOWN',
                    thumbnail = book['thumbnailUrl'] if 'thumbnailUrl' in book else '',
                    published_date = book['publishedDate']['$date'] if 'publishedDate' in book else None
                )

                new_book.save()
                new_book.authors.set(authors)
                new_book.categories.set(categories)

        new_application = Application(
            name = 'Main App',
            authorization_grant_type = AbstractApplication.GRANT_PASSWORD,
            client_type = AbstractApplication.CLIENT_CONFIDENTIAL
        )
        new_application.save()

        new_user = User.objects.create_superuser(email = 'admin@admin.cl', password = '1')
        new_user.save()
