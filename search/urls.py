from django.urls import path
from rest_framework.routers import DefaultRouter

from articles.views import ArticleDocumentView
from search.views import SearchArticles

router = DefaultRouter()
router.register("article", ArticleDocumentView, basename="article")

urlpatterns = [
    path("article-search/<str:query>/", SearchArticles.as_view()),
]