import requests
import os, time
from tqdm import tqdm
from bs4 import BeautifulSoup
import json
headers={
  'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:70.0) Gecko/20100101 Firefox/70.0'
}
DataList = []
id = 0
'''
[
    {
        "id": 1,
        "name": "麻婆豆腐",
        "cuisine": "川菜",
        "cooking_method": "炖",
        "taste": "麻辣味",
        "image_url":"https://st-cn.meishij.net/r/41/203/113291/a113291_40378.jpg",
        
    },
]

'''

def getcuisineinfo(cuisine_url, cuisine_category):
    global id
    global DataList
    print("==============正在爬取{}信息============".format(cuisine_category))
    cuisine_html = requests.get(cuisine_url, headers=headers)
    soup = BeautifulSoup(cuisine_html.text, 'lxml')

    dish_data = soup.select('html>body>div.main_w.clearfix>div.main>div.liststyle1_w.clearfix>div.listtyle1_w>div.listtyle1_list.clearfix>div.listtyle1>a.big')

    for info in dish_data:
        dish_info = {}
        dish_id = id
        id = id + 1
        dish_name = info['title']
        dish_cuisine = cuisine_category
        dish_cooking_method = info.div.div.find_all("div")[-1].ul.find_all("li")[-1].string.split(" / ")[0]
        dish_taste = info.div.div.find_all("div")[-1].ul.find_all("li")[-1].string.split(" / ")[1]
        dish_img_url = info.img["src"]

        dish_info["id"] = dish_id
        dish_info["name"] = dish_name
        dish_info["cuisine"] = dish_cuisine
        dish_info["cooking_method"] = dish_cooking_method
        dish_info["taste"] = dish_taste
        dish_info["image_url"] = dish_img_url
        DataList.append(dish_info)



    page_data = soup.select('html>body>div.main_w.clearfix>div.main>div.liststyle1_w.clearfix>div.listtyle1_w>div.listtyle1_page>div.listtyle1_page_w>a.next')
    if len(page_data) == 0:
        return
    else:
        next_url = page_data[0]["href"]
        getcuisineinfo(next_url, cuisine_category)


if __name__ == '__main__':
    # global DataList
    url = 'https://www.meishij.net/china-food/caixi/chuancai/'
    main_html = requests.get(url,headers=headers)        #Get方式获取网页数据
    soup = BeautifulSoup(main_html.text, 'lxml')
    data = soup.select('html>body>div.main_w.clearfix>div.main>div.listnav.clearfix>div.other_c.listnav_con.clearfix>dl.listnav_dl_style1.w990.clearfix>dd')
    for index, info in enumerate(data):
        # print(info.a["href"], info.a.string)
        getcuisineinfo(info.a["href"], info.a.string)

    json_str = json.dumps(DataList, ensure_ascii=False)
    with open(os.path.join('./data/', "allData.json"), 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)