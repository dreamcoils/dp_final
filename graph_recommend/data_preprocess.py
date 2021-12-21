import json

with open("../data/allData.json", encoding="utf-8") as file:
    load_dict = json.load(file)

entities_id = {}
entities_relation = {}
id_generator = 0

# 为知识图谱中的每个实体设置entity_id
for e in load_dict:
    name = e['name']
    taste = e['taste']
    cuisine = e['cuisine']
    cooking_method = e['cooking_method']
    if name not in entities_id:
        entities_id[name] = id_generator
        id_generator = id_generator + 1
    if taste not in entities_id:
        entities_id[taste] = id_generator
        id_generator = id_generator + 1
    if cuisine not in entities_id:
        entities_id[cuisine] = id_generator
        id_generator = id_generator + 1
    if cooking_method not in entities_id:
        entities_id[cooking_method] = id_generator
        id_generator = id_generator + 1

# 将知识图谱中的数据以<head-relation-tail>的格式存入文件中
with open("../data/kg.txt", "w") as f:
    for e in load_dict:
        f.write(e['name'] + " taste " + e['taste'] + "\n")
        f.write(e['name'] + " cuisine " + e['cuisine'] + "\n")
        f.write(e['name'] + " cooking_method " + e['cooking_method'] + "\n")

f.close()
print("finish")
