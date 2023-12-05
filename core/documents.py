# import Elastic
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

# import target model
from .models import Article

@registry.register_document
class ArticleDocument(Document):
    class Index:
        pass

    class Django:
        model = Article # model associated to the document
        fields = [
            'title',
            'summary',
        ]
        pass
