import requests
import re
import chompjs
import os


base_url = 'https://ssr.res.netease.com/pc/zt/20191112204330/'

# get infomation of shishen
info_url = base_url + 'js/index_7d046f37.js'
req = requests.get(url=info_url)
pattern = re.compile(r'd=\[(.*?)\];func')
name_list = pattern.findall(req.text)[0]
name_json = chompjs.parse_js_object('[' + name_list + ']')

"""
img_url = 'e.dataPath + "data/card/" + e.bigCardId + ".png?19"'
e.dataPath = 'https://ssr.res.netease.com/pc/zt/20191112204330/'
e.bigCardId = img_id
"""
 
# get img
for elem in name_json:
    img_name = elem.get("name")
    shishen_id = elem.get("id")
    img_url = base_url + "data/card/" + str(shishen_id) + ".png?19"
    img_req = requests.get(img_url)

    global shishen_name
    if elem.get('type') == '式神':
        shishen_name = elem.get('name')
        try:
            # make dirctory of shishen
            os.mkdir(f'./imgs/{shishen_name}')
        except FileExistsError:
            pass
        except FileNotFoundError:
            shishen_name = shishen_name.replace('/', '_')
            os.mkdir(f'./imgs/{shishen_name}')

    else:
        try:
            with open(f'./imgs/{shishen_name}/{img_name}', 'wb') as fp:
                fp.write(img_req.content)
        except FileNotFoundError:
            img_name = img_name.replace('/', '_')
            with open(f'./imgs/{shishen_name}/{img_name}', 'wb') as fp:
                fp.write(img_req.content)

    print(img_name)
