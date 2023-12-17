from django.urls import path, include
from rest_framework.routers import DefaultRouter

from articles.views import ArticleDocumentView

router = DefaultRouter()
router.register("article", ArticleDocumentView, basename="article")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += router.urls
