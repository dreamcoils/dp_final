import cv2
import torch
from PIL import Image
import glob
import clip
import heapq

def find_topK_matches(photo_features, text_features, text_names, k):
    mat = photo_features @ torch.t(text_features)
    print(mat)
    array = mat.numpy()
    max_indexs = heapq.nlargest(k, range(len(array)), array.__getitem__)
    return [text_names[index] for index in max_indexs]



def main():
    device = "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

    ## text feature load
    text_features, text_names = torch.load('./features/dish_name_features.pth')
    print(text_features.shape)

    ## image feature extract
    pic_path = "E:\软微\课程\研一上\海量数据处理\project\data\馒头.png"

    with torch.no_grad():
        frame = Image.open(pic_path)
        cover_image = preprocess(frame).unsqueeze(0).to(device)
        photo_features = model.encode_image(cover_image)
        photo_features /= photo_features.norm(dim=-1, keepdim=True)
        photo_features = photo_features.detach().cpu().squeeze(0)
    print(photo_features.shape)
    best_dish_names = find_topK_matches(photo_features, text_features, text_names, 5)
    print(best_dish_names)


if __name__ == '__main__':
    main()


