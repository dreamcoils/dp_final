import json
import pandas as pd
import random


def format_data():
    with open("../data/allData.json", encoding="utf-8") as json_data:
        load_dict = json.load(json_data)
    json_data.close()

    entity_dict = {}
    with open("../data/entity_id.txt", encoding="utf-8") as file:
        for line in file.readlines():
            tuple = line.split("\t")
            entity_dict[tuple[0]] = tuple[1].split("\n")[0]

    with open("../data/item_detail.txt", "w") as f:
        for e in load_dict:
            f.write(str(entity_dict[e['name']]) + "\t" + e['name'] + "\t" + e['taste'] + "\t" +
                    e['cuisine'] + "\t" + e['cooking_method'] + "\t" + e['image_url'] + "\n")
    f.close()


def format_kg():
    with open("../data/allData.json", encoding="utf-8") as f1:
        load_dict = json.load(f1)
    f1.close()

    entities_dict = {}
    id_generator = 0

    # 为知识图谱中的每个实体设置entity_id
    for e in load_dict:
        name = e['name']
        taste = e['taste']
        cuisine = e['cuisine']
        cooking_method = e['cooking_method']
        if name not in entities_dict:
            entities_dict[name] = id_generator
            id_generator = id_generator + 1
        if taste not in entities_dict:
            entities_dict[taste] = id_generator
            id_generator = id_generator + 1
        if cuisine not in entities_dict:
            entities_dict[cuisine] = id_generator
            id_generator = id_generator + 1
        if cooking_method not in entities_dict:
            entities_dict[cooking_method] = id_generator
            id_generator = id_generator + 1

    # 将知识图谱中的数据以<head-relation-tail>的格式存入文件中
    with open("../data/kg.txt", "w") as f1:
        for e in load_dict:
            f1.write(str(entities_dict[e['name']]) + "\ttaste\t" + str(entities_dict[e['taste']]) + "\n")
            f1.write(str(entities_dict[e['name']]) + "\tcuisine\t" + str(entities_dict[e['cuisine']]) + "\n")
            f1.write(
                str(entities_dict[e['name']]) + "\tcooking_method\t" + str(entities_dict[e['cooking_method']]) + "\n")
    f1.close()

    with open("../data/entity_id.txt", "w") as f2:
        for k, v in entities_dict.items():
            f2.write(str(k) + "\t" + str(v) + "\n")
    f2.close()


def test_data_generator():
    '''
    生成测试数据函数
    生成方法（思路基于LDA）：对于测试用户u，以某概率生成u喜爱的菜品类别分布，再以某概率生成每一个菜品类别下具体的菜品分布。
    :return:
    '''
    with open("../data/allData.json", encoding="utf-8") as file:
        load_dict = json.load(file)
    file.close()

    entity_dict = {}
    with open("../data/entity_id.txt", encoding="utf-8") as file:
        for line in file.readlines():
            tuple = line.split("\t")
            entity_dict[tuple[0]] = tuple[1].split("\n")[0]

    dict = {}
    for e in load_dict:
        if e['cuisine'] not in dict:
            dict[e['cuisine']] = [e['name']]
        else:
            dict[e['cuisine']].append(e['name'])

    with open("../data/user_item.txt", "w") as f1:
        cuisines = list(dict.keys())
        user_num = 1000
        for num in range(user_num):
            topic_quantities = random.randint(1, 2)
            favorite_topics = random.sample(range(0, len(cuisines)), topic_quantities)
            for topic in favorite_topics:
                food_quantities = random.randint(1, 15)
                food_num = len(dict[cuisines[topic]])
                favorite_foods = random.sample(range(0, food_num), min(food_quantities, food_num))
                for food in favorite_foods:
                    food_name = dict[cuisines[topic]][food]
                    food_id = entity_dict[food_name]
                    f1.write(str(num) + "\t" + str(food_id) + "\t" + "1\n")


if __name__ == '__main__':
    format_data()
    # format_kg()
    # test_data_generator()
    chart = pd.read_csv("../data/item_detail.txt", sep='\t', names=["taste", "cuisine", "cooking_method", "url"])
    print()
