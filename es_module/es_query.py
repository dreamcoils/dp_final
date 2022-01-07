from elasticsearch import Elasticsearch
from basic_structure.Entity import Food
import json


def query(s):
    es = Elasticsearch([{'host': '39.101.165.8', 'port': 9200}])

    query_str = {
        "query": {
            "match": {
                "name": s
            }
        }
    }

    response = es.search(index='foods', doc_type='_doc', body=query_str)
    res = []
    for item in response['hits']['hits']:
        item = item['_source']
        name = item['name']
        cuisine = item['cuisine']
        cooking_method = item['cooking_method']
        taste = item['taste']
        image_url = item['image_url']
        f = Food(name, cuisine, cooking_method, taste, image_url)
        res.append(f.__dict__)
    return json.dumps(res, ensure_ascii=False)


if __name__ == '__main__':
    result = query("鸡")
    print()
