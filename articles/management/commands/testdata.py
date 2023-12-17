from django.core.management import BaseCommand
from articles.models import Article, Author, Pdf, ArticleAuthor
from articles.documents import ArticleDocument


class Command(BaseCommand):
    help = 'Create dummy data for testing'

    def handle(self, *args, **kwargs):
        # Create some Pdf instances
        pdf1 = Pdf.objects.create(url="http://example.com/pdf1")
        pdf2 = Pdf.objects.create(url="http://example.com/pdf2")

        # Create some Author instances
        author1 = Author.objects.create(first_name="John", last_name="Doe")
        author2 = Author.objects.create(first_name="Jane", last_name="Doe")

        # Create some Article instances
        article1 = Article.objects.create(pdf_url=pdf1)
        article2 = Article.objects.create(pdf_url=pdf2)

        # Create some ArticleAuthor instances
        ArticleAuthor.objects.create(author=author1, article=article1)
        ArticleAuthor.objects.create(author=author2, article=article2)

        # Index the Article instances in Elasticsearch
        ArticleDocument().update(Article.objects.all())
