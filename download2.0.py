import aiohttp
import asyncio
import re
import chompjs
import os

import requests

base_url = 'https://ssr.res.netease.com/pc/zt/20191112204330/'

# get information of shishen
info_url = base_url + 'js/index_7d046f37.js'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def download_img(session, shishen_name, img_name, shishen_id):
    img_url = base_url + "data/card/" + str(shishen_id) + ".png?19"
    async with session.get(img_url) as img_response:
        img_content = await img_response.content.read()
        try:
            with open(f'./imgs/{shishen_name}/{img_name}', 'wb') as fp:
                fp.write(img_content)
        except FileNotFoundError:
            img_name = img_name.replace('/', '_')
            with open(f'./imgs/{shishen_name}/{img_name}', 'wb') as fp:
                fp.write(img_content)


async def download_all_images(shishen_list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for elem in shishen_list:
            img_name = elem.get("name")
            shishen_id = elem.get("id")

            if elem.get('type') == '式神':
                shishen_name = elem.get('name')
                try:
                    # make directory of shishen
                    os.mkdir(f'./imgs/{shishen_name}')
                except FileExistsError:
                    pass
                except FileNotFoundError:
                    shishen_name = shishen_name.replace('/', '_')
                    os.mkdir(f'./imgs/{shishen_name}')

            else:
                task = asyncio.create_task(download_img(session, shishen_name, img_name, shishen_id))
                tasks.append(task)

        await asyncio.gather(*tasks)


async def main():
    req = requests.get(url=info_url)
    pattern = re.compile(r'd=\[(.*?)\];func')
    name_list = pattern.findall(req.text)[0]
    name_json = chompjs.parse_js_object('[' + name_list + ']')
    await download_all_images(name_json)


if __name__ == '__main__':
    asyncio.run(main())
