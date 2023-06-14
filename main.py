from typing import Dict, Any
import uvicorn
import os
import argparse
from urllib.request import urlretrieve

from fastapi import FastAPI, File, UploadFile
from fastapi.param_functions import Form
from pydantic import BaseModel

from config import UPLOAD_PATH, TOP_K
from log import LOGGER
from image_search import do_image_search
from text_search import do_text_search
from insert_image import do_insert
from milvus_collection import set_collection


if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)
    LOGGER.info(f"make the dir: {UPLOAD_PATH}")


app = FastAPI()


@app.post('/img/search')
async def image_search(image: UploadFile = File(...), topk: int = Form(TOP_K)):
    try:
        content = await image.read()
        print('read pic succ')
        img_path = os.path.join(UPLOAD_PATH, image.filename)
        with open(img_path, "wb+") as f:
            f.write(content)
        res = do_image_search(img_path)
        LOGGER.info("Successfully searched similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/path/search')
async def path_search(path: str, topk: int = Form(TOP_K)):
    try:
        res = do_image_search(path)
        LOGGER.info("Successfully searched similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/text/search')
async def text_search(text: str, topk: int = Form(TOP_K)):
    try:
        res = do_text_search(text)
        LOGGER.info("Successfully searched similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400


# @app.post('/img/insert')
# async def insert_image(image: UploadFile = File(None), url: str = None, sku_data: SKU = None):
#     try:
#         # Save the upload image to server.
#         if image is not None:
#             content = await image.read()
#             print('read pic succ')
#             img_path = os.path.join(UPLOAD_PATH, image.filename)
#             with open(img_path, "wb+") as f:
#                 f.write(content)
#         elif url is not None:
#             img_path = os.path.join(UPLOAD_PATH, os.path.basename(url))
#             urlretrieve(url, img_path)
#         else:
#             return {'status': False, 'msg': 'Image and url are required'}, 400
#         img_id = do_insert(img_path, sku_data)
#         LOGGER.info(f"Successfully uploaded data, image id: {img_id}")
#         return "Successfully loaded data: " + str(img_id)
#     except Exception as e:
#         LOGGER.error(e)
#         return {'status': False, 'msg': e}, 400


# def parse_arguments():
#     parser = argparse.ArgumentParser(description='Script description.')
#     parser.add_argument('--load_csv', action='store_true',
#                         help='Flag to enable loading images from CSV.')
#     parser.add_argument('--load_img_root_path', type=str, required=False, default=None,
#                         help='Root path for loading images.')
#     args = parser.parse_args()
#     return args


if __name__ == '__main__':
    # args = parse_arguments()
    set_collection()
    uvicorn.run(app=app, host='localhost', port=5000)
