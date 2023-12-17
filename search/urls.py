from django.urls import path

from search.views import SearchArticles

urlpatterns = [
    path("article-search/<str:query>/", SearchArticles.as_view()),
]