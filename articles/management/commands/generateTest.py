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


# the one created with copilot

import requests
import json
from faker import Faker
from articles.signals import create_article_in_elasticsearch
from articles.models import Article

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
    data["institutions"] = [{"name": fake.company()} for _ in range(2)]
    data["publish_date"] = str(fake.date_between(start_date='-1y', end_date='today'))

    # Create the article in Elasticsearch and get the Elasticsearch ID
    elasticsearch_id = create_article_in_elasticsearch(data)

    # Create the Article instance and save it
    article = Article(elasticsearch_id=elasticsearch_id, **data)
    article.save()

    # Print the Elasticsearch ID
    print(f"Document {_+1}: {article.elasticsearch_id}")
