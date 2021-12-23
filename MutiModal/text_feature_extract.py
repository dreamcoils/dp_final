import json
import clip
import torch
import numpy as np

def encode_search_query(search_query, model):
    with torch.no_grad():
        model=model.float()
        # Encode and normalize the search query using CLIP
        text_encoded = model.encode_text(clip.tokenize(search_query).to("cpu"))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)
    # Retrieve the feature vector from the GPU and convert it to a numpy array
    return text_encoded.cpu()


if __name__ == '__main__':
    with open("E:\\软微\\课程\\研一上\\海量数据处理\\project\\data\\allDataNew.json", 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)

    device = "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

    features = []
    dish_name = []

    for data in json_data:
        dish_feat = encode_search_query(data["eng_name"], model)
        dish_feat = dish_feat.squeeze(0).to(device)
        features.append(dish_feat)
        dish_name.append(data["name"])
        print(data["name"])

    features = torch.stack(features, dim=0)
    torch.save((features, dish_name), './features/dish_name_features.pth')