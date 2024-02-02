from django.db import models


# Create your models here.


# class Institution(models.Model):
#     class Meta:
#         db_table = 'institution'
#
#
# class Pdf(models.Model):
#     url = models.CharField(primary_key=True, max_length=255)
#
#     class Meta:
#         db_table = 'pdf'


class Article(models.Model):
    elasticsearch_id = models.CharField(max_length=255, blank=True, null=True)

    # to know that the article hasn't been indexed yet

    # def save(self, *args, **kwargs):
    #     from .signals import create_article_in_elasticsearch
    #     # Prepare the article data for Elasticsearch
    #     article_data = {
    #         'id': self.id,
    #     }
    #     # Create the article in Elasticsearch and get the Elasticsearch ID
    #     elasticsearch_id = create_article_in_elasticsearch(article_data)
    #     # Set the elasticsearch_id field
    #     self.elasticsearch_id = elasticsearch_id
    #     # Call the original save method
    #     super().save(*args, **kwargs)

    class Meta:
        managed = True  # TODO: check whether I need to reverse it back to False

# class ArticleAuthor(models.Model):
#     author = models.ForeignKey('Author', models.DO_NOTHING, db_column='author_ID')
#     article = models.ForeignKey(Article, models.DO_NOTHING)
#
#     class Meta:
#         db_table = 'article_author'
#         unique_together = (('author', 'article'),)
#
#
# class Author(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#
#     class Meta:
#         db_table = 'author'
