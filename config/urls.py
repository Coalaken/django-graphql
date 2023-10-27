from django.contrib import admin
from graphene_django.views import GraphQLView
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True))
]
