from django.core.management.base import BaseCommand

# from articles.documents import ArticleDocument
from elasticsearch import Elasticsearch

# create an instance of Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"],http_auth=('elastic', '-T9NxlPBzHTru8L6+4mY'))
# sudo docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

class Command(BaseCommand):
    help = "Clear the elasticsearch database"

    def handle(self, *args, **options):

        # delete all existing documents
        es.delete_by_query(
            index='articles',
            query={
                "match_all": {}
            }
        )
