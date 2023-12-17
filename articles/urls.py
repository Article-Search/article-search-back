from django.urls import path, include
from rest_framework import routers

from articles.views import ArticleDocumentView

router = routers.DefaultRouter()
router.register(r"article", ArticleDocumentView)

urlpatterns = [
    path("", include(router.urls)),
]