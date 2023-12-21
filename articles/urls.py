from django.urls import path, include
from rest_framework.routers import DefaultRouter

from articles.views import ArticleDocumentView

router = DefaultRouter()
router.register(r"articles", ArticleDocumentView, basename="articles")

urlpatterns = [
    path("", include(router.urls)),
]

# urlpatterns += router.urls
