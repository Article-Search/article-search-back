# import requests
# import json
# from faker import Faker
#
# fake = Faker()
#
# # Define the base data structure
# base_data = {
#     "title": "",
#     "authors": [],
#     "keywords": [],
#     "content": "",
#     "institutions": [],
#     "publish_date": "",
# }
#
# # Define the URL for the POST requests
# url = "http://localhost:9200/articles/_doc/"
#
# # Generate and send 20 documents
# for _ in range(20):
#     # Generate fake data
#     data = base_data.copy()
#     data["title"] = fake.sentence()
#     data["authors"] = [{"first_name": fake.first_name(), "last_name": fake.last_name()} for _ in range(2)]
#     data["keywords"] = [fake.word() for _ in range(2)]
#     data["content"] = fake.text()
#     data["institutions"] = [{"name": fake.company()} for _ in range(2)]
#     data["publish_date"] = str(fake.date_between(start_date='-1y', end_date='today'))
#
#     # Send the POST request
#     response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
#
#     # Print the response status code
#     print(f"Document {_+1}: {response.status_code}")
import uuid

# the one created with copilot

from django.core.management.base import BaseCommand
from faker import Faker
from articles.signals import create_article_in_elasticsearch
from articles.models import Article


class Command(BaseCommand):
    help = 'Generates test data and adds it to Elasticsearch and the database'

    def handle(self, *args, **options):
        fake = Faker()

        # Define the base data structure
        base_data = {
            "title": "",
            "authors": [],
            "keywords": [],
            "content": "",
            "institutions": [],
            "publish_date": "",
        }

        # Generate and create 20 articles
        for _ in range(20):
            # Generate fake data
            data = base_data.copy()
            data["title"] = fake.sentence()
            data["authors"] = [{"first_name": fake.first_name(), "last_name": fake.last_name()} for _ in range(2)]
            data["keywords"] = [fake.word() for _ in range(2)]
            data["content"] = fake.text()
            data["summary"] = fake.text()
            data["pdf_url"] = fake.url()
            data["institutions"] = [{"name": fake.company()} for _ in range(2)]
            data["references"] = [{"title": fake.address()} for _ in range(2)]
            data["publish_date"] = str(fake.date_between(start_date='-30y', end_date='today'))

            # Create the article in Elasticsearch and get the Elasticsearch ID
            elasticsearch_id = create_article_in_elasticsearch(data)

            # Create the Article instance and save it
            article = Article(elasticsearch_id=elasticsearch_id)
            article.save()

            # Print the Elasticsearch ID
            self.stdout.write(f"Document {_ + 1}: {article.elasticsearch_id}")
