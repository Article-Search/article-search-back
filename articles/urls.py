from django.urls import path, include
from rest_framework.routers import DefaultRouter

from articles.views import ArticleDocumentView

router = DefaultRouter()
router.register(r"articles", ArticleDocumentView, basename="articles")

urlpatterns = [
    # this route provide exact word searching, exact keywords filtering, suggestions in searches
    path("", include(router.urls)),
]

# urlpatterns += router.urls


"""
GET requests for the articles app:
!!! ALWAYS SEARCH WITH lowercase letters

1. **Listing all articles**:
    - URL: http://127.0.0.1:8000/articles/
    - Description: Returns a list of all articles ordered by the `publish_date` field in descending order.

2. **Searching for articles**:
    - URL: http://127.0.0.1:8000/articles/?search={query}
    - Example: http://127.0.0.1:8000/articles/?search=python
    - Description: Returns a list of articles that match the search term in the "title", "keywords", "content", "authors.first_name", "authors.last_name", and "institutions.name" fields.

3. **Filtering articles**:
    - URL: http://127.0.0.1:8000/articles/?{field}={value}
    - Description: Returns a list of articles that match the filter. Available fields for filtering are "keywords", "author_first_name", "author_last_name", "institution_name", and "publish_date".

4. **Suggesting articles**:
    - URL: http://127.0.0.1:8000/articles/?suggest={field}&suggest_text={text}
    - Example: http://127.0.0.1:8000/articles/?suggest=title_suggest&suggest_text=django
    - Description: Returns a list of suggested articles. Available fields for suggestions are "title_suggest", "authors_first_name_suggest", "authors_last_name_suggest", "institution_name_suggest", "content_suggest", and "summary_suggest".

5. **Faceted search on articles**:
    - URL: http://127.0.0.1:8000/articles/?facet={field}
    - Description: Returns a list of articles along with the facet counts for the specified field. Available field for faceted search is "keywords".

6. **Filtering articles by a range of dates**:
    - URL: http://127.0.0.1:8000/articles/?publish_date__gte={start_date}&publish_date__lte={end_date}
    - Description: Returns a list of articles that were published between the start date and the end date.

7. **Filtering articles by a date greater than or equal to**:
    - URL: http://127.0.0.1:8000/articles/?publish_date__gte={date}
    - Description: Returns a list of articles that were published on or after the specified date.

8. **Filtering articles by a date less than or equal to**:
    - URL: http://127.0.0.1:8000/articles/?publish_date__lte={date}
    - Description: Returns a list of articles that were published on or before the specified date.

Note: Replace {query}, {field}, {value}, {start_date}, {end_date}, and {date} with your actual values. Dates should be in the "YYYY-MM-DD" format.
"""
