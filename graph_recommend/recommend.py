import pandas as pd
import torch
import argparse
import json
import os

from basic_structure.Entity import Food
from graph_recommend.data_loader import DataLoader

from graph_recommend.kgcn_model import KGCN


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', type=str, default='food', help='which dataset to use')
    parser.add_argument('--aggregator', type=str, default='sum', help='which aggregator to use')
    parser.add_argument('--n_epochs', type=int, default=80, help='the number of epochs')
    parser.add_argument('--neighbor_sample_size', type=int, default=8, help='the number of neighbors to be sampled')
    parser.add_argument('--dim', type=int, default=16, help='dimension of user and entity embeddings')
    parser.add_argument('--n_iter', type=int, default=1,
                        help='number of iterations when computing entity representation')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size')
    parser.add_argument('--l2_weight', type=float, default=1e-4, help='weight of l2 regularization')
    parser.add_argument('--lr', type=float, default=5e-4, help='learning rate')
    parser.add_argument('--ratio', type=float, default=0.8, help='size of training dataset')

    args = parser.parse_args(['--l2_weight', '1e-4'])
    return args


def get_dataloader():
    args = get_args()
    data_loader = DataLoader(args.dataset)
    return data_loader


def get_load_model(path):
    data_loader = get_dataloader()
    kg = data_loader.load_kg()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    num_user, num_entity, num_relation = data_loader.get_num()
    loaded_model = KGCN(num_user, num_entity, num_relation, kg, get_args(), device)
    loaded_model.load_state_dict(torch.load(path))
    loaded_model.eval()
    return loaded_model


def rec_foods(user_id, path):
    user_id = int(user_id)
    df_rating = pd.read_csv("data/user_item.txt", sep='\t', header=None, names=['userID', 'itemID', 'rating'])
    chart = pd.read_csv("data/item_detail.txt", sep='\t', header=None,
                        names=['id', 'name', 'taste', 'cuisine', 'cooking_method', 'url'])
    item_ids = chart['id']
    fav_foods = df_rating[df_rating['userID'] == user_id]['itemID']

    model = get_load_model(path)
    user = torch.tensor([user_id])
    score_list = []
    for id in item_ids:
        if id not in fav_foods.values.tolist():
            item = torch.tensor([id])
            score = model(user, item)
            score_list.append([id, score])

    sort_list = sorted(score_list, key=lambda t: t[1], reverse=True)

    res = []
    for t in sort_list[:10]:
        id = t[0]
        cur_item = chart[chart['id'].isin([id])]
        cur_item.reset_index(inplace=True, drop=True)
        name = cur_item.at[0, 'name']
        cuisine = cur_item.at[0, 'cuisine']
        cooking_method = cur_item.at[0, 'cooking_method']
        taste = cur_item.at[0, 'taste']
        image_url = cur_item.at[0, 'url']
        f = Food(name, cuisine, cooking_method, taste, image_url)
        res.append(f.__dict__)
    return json.dumps(res, ensure_ascii=False)
