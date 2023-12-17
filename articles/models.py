from django.db import models


# Create your models here.


class Institution(models.Model):
    class Meta:
        managed = False
        db_table = 'institution'


class Pdf(models.Model):
    url = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'pdf'


class Article(models.Model):
    pdf_url = models.ForeignKey('Pdf', models.DO_NOTHING, db_column='pdf_url')
    authors = models.ManyToManyField('Author', through='ArticleAuthor')

    class Meta:
        managed = False
        db_table = 'article'


class ArticleAuthor(models.Model):
    author = models.ForeignKey('Author', models.DO_NOTHING, db_column='author_ID')
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'article_author'
        unique_together = (('author', 'article'),)


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'author'


