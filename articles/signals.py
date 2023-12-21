# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
#
# from django_elasticsearch_dsl.registries import registry
#
#
# @receiver(post_save)
# def update_document(sender, **kwargs):
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']
#
#     if app_label == 'articles':
#         if model_name == 'article':
#             instances = instance.article.all()
#             for _instance in instances:
#                 registry.update(_instance)
#
#
# @receiver(post_delete)
# def delete_document(sender, **kwargs):
#     app_label = sender._meta.app_label
#     model_name = sender._meta.model_name
#     instance = kwargs['instance']
#
#     if app_label == 'articles':
#         if model_name == 'article':
#             instances = instance.article.all()
#             for _instance in instances:
#                 registry.update(_instance)

from elasticsearch_dsl.connections import connections
from articles.documents import ArticleDocument

# Create a connection to Elasticsearch
connections.create_connection(hosts='https://localhost:9200', timeout=20)
# TODO: change it in production
def create_article_in_elasticsearch(article_data):
    # Create the article in Elasticsearch
    article = ArticleDocument(meta={'id': article_data['id']})
    for field, value in article_data.items():
        setattr(article, field, value)
    article.save()
    return article.meta.id
