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
from set_collection import set_collection
from prepare_collection import prepare_collection


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


def parse_arguments():
    parser = argparse.ArgumentParser(description='Script description.')
    parser.add_argument('--csv', type=str, required=True, help='path to sku data.')
    parser.add_argument('--root', type=str, required=True, help='Root path for loading images.')
    parser.add_argument('--num', type=int, required=False, default=100, help='Number of insert images.')
    parser.add_argument('--purge', type=bool, required=False, default=True, help='Whether to clear existing collection.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    set_collection(args.purge)
    prepare_collection(args.csv, args.root, args.num)
    uvicorn.run(app=app, host='localhost', port=5000)
