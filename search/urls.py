from django.urls import path

from search.views import SearchArticles

urlpatterns = [
    # This route provide search option with fuzziness if someone makes typos
    path("article-search/<str:query>/", SearchArticles.as_view()),
]

"""
GET requests for the search app:

1. **Searching for articles**:
    - URL: http://127.0.0.1:8000/articles/article-search/{query}/
    - Description: Returns a list of articles that match the search term. The search is performed on the fields "title", "keywords", "content", "authors.first_name", "authors.last_name", and "institutions.name". The results are paginated and ordered by the `publish_date` field in descending order.
    -It also supports fuzziness if someone makes typos
    -Example: http://127.0.0.1:8000/article-search/Django/ To search for articles that contain the word "django"

Note: Replace {query} with your actual search term.
"""
