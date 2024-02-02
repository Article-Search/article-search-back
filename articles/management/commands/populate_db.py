from django.core.management.base import BaseCommand

from articles.models import Article


class Command(BaseCommand):
    help = "Populates the database with some testing data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Started database population process..."))

        # Create articles
        website_article = Article.objects.create()
        website_article.save()

        google_article = Article.objects.create()
        google_article.save()

        programming_article = Article.objects.create()
        programming_article.save()

        ubuntu_article = Article.objects.create()
        ubuntu_article.save()

        django_article = Article.objects.create()
        django_article.save()

        self.stdout.write(self.style.SUCCESS("Successfully populated the database."))
