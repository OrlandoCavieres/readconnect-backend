"""
URL configuration for ReadConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from strawberry.django.views import GraphQLView

from ReadConnect.main_schema import schema


urlpatterns = [
    # Admin site routes urls
    path('admin/', admin.site.urls),

    # Oauth2 Authentication and Authorization urls
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # GraphQL playground and main endpoint connection url
    re_path(r'^api/graphql/?$', GraphQLView.as_view(schema = schema)),
]
