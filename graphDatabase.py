from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123456"))

def add_categories(tx, dish_name, category):
    tx.run("MERGE (a:Dish {name: $dish_name}) "
           "MERGE (c:Cuisine {category: $category}) "
           "MERGE (a)-[:IS]->(c)",
           dish_name=dish_name, category=category)

def add_cooking_method(tx, dish_name, cooking_method):
    tx.run("MERGE (a:Dish {name: $dish_name}) "
           "MERGE (c:Cooking_Method {method: $cooking_method}) "
           "MERGE (a)-[:HOW_TO_COOK]->(c)",
           dish_name=dish_name, cooking_method=cooking_method)

def add_taste(tx, dish_name, taste):
    tx.run("MERGE (a:Dish {name: $dish_name}) "
           "MERGE (t:Taste {taste: $taste}) "
           "MERGE (a)-[:STYLE]->(t)",
           dish_name=dish_name, taste=taste)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])


with driver.session() as session:
    with open("./data/allData.json", "r",encoding='utf-8') as fr:
        load_list = json.load(fr)
        for index, dic in enumerate(load_list):
            print(index)
            session.write_transaction(add_categories,dic["name"], dic["cuisine"])
            session.write_transaction(add_cooking_method, dic["name"], dic["cooking_method"])
            session.write_transaction(add_taste, dic["name"], dic["taste"])

# session.write_transaction(add_friend, "Arthur", "Guinevere")
# session.write_transaction(add_friend, "Arthur", "Lancelot")
# session.write_transaction(add_friend, "Arthur", "Merlin")
# session.read_transaction(print_friends, "Arthur")
# session.read_transaction(print_friends, "Guinevere")
