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
    institution = models.ForeignKey('Institution', models.DO_NOTHING)
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'article'


class ArticleAuthor(models.Model):
    author = models.OneToOneField('Author', models.DO_NOTHING, db_column='author_ID', primary_key=True)  # Field name made lowercase. The composite primary key (author_ID, article_id) found, that is not supported. The first column is selected.
    article = models.ForeignKey(Article, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'article_author'
        unique_together = (('author', 'article'),)


class Author(models.Model):

    class Meta:
        managed = False
        db_table = 'author'
