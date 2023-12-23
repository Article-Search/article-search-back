# import Elastic
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

# import target model
from .models import Article


@registry.register_document
class ArticleDocument(Document):
    publish_date = fields.DateField()
    title = fields.TextField(
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    authors = fields.NestedField(properties={
        'first_name': fields.TextField(
            fields={
                'raw': fields.TextField(),
                'suggest': fields.CompletionField(),
            }
        ),
        'last_name': fields.TextField(
            fields={
                'raw': fields.TextField(),
                'suggest': fields.CompletionField(),
            }
        ),
    })

    institutions = fields.NestedField(properties={
        'name': fields.TextField(
            fields={
                'raw': fields.TextField(),
                'suggest': fields.CompletionField(),
            }
        ),
    })
    summary = fields.TextField(
        # TODO: Check whether I'll leave the suggestion part to optimize the index performance
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    keywords = fields.KeywordField(multi=True)
    content = fields.TextField(
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )

    pdf_url = fields.TextField()
    references = fields.NestedField(properties={
        'title': fields.TextField(
            fields={
                'raw': fields.TextField(),
                'suggest': fields.CompletionField(),
            }
        )
    })

    class Index:
        name = 'articles'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Article

    # def prepare_title(self, instance):
    #     # Retrieve title from Elasticsearch
    #     pass
    #
    # def prepare_publish_date(self, instance):
    #     # Retrieve publish_date from Elasticsearch
    #     pass
    #
    # def prepare_keywords(self, instance):
    #     # Retrieve keywords from Elasticsearch
    #     pass
    #
    # def prepare_integral_text(self, instance):
    #     # Retrieve integral_text from Elasticsearch
    #     pass
