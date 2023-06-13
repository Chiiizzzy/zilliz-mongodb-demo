from typing import Dict
import uvicorn
import os
import argparse
from fastapi import FastAPI, File, UploadFile
from fastapi.param_functions

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)
    LOGGER.info(f"mkdir the path:{UPLOAD_PATH}")

@app.post('/img/search')
async def search_images(image: UploadFile = File(...), topk: int = Form(TOP_K), table_name: str = None):
    try:
        #TODO search similar image logic
        
        LOGGER.info("Successfully searched similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400

@app.post('/text/search')
async def search_text(text: str, topk: int = Form(TOP_K), table_name: str = None):
    try:
        #TODO search similar text logic
        LOGGER.info("Successfully searched similar images!")
        return res
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400

@app.post('/img/upload')
async def upload_items(image: UploadFile = File(None), url: str = None, meta_info = Dict, table_name: str = None):
    try:
        # Save the upload image to server.
        if image is not None:
            content = await image.read()
            print('read pic succ')
            img_path = os.path.join(UPLOAD_PATH, image.filename)
            with open(img_path, "wb+") as f:
                f.write(content)
        elif url is not None:
            img_path = os.path.join(UPLOAD_PATH, os.path.basename(url))
            urlretrieve(url, img_path)
        else:
            return {'status': False, 'msg': 'Image and url are required'}, 400
        #TODO implement upload image, meta_info record.     
        #vector_id = do_upload(table_name, img_path, MODEL, MILVUS_CLI, MYSQL_CLI)
        LOGGER.info(f"Successfully uploaded data, vector id: {vector_id}")
        return "Successfully loaded data: " + str(vector_id)
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}, 400

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script description.')
    parser.add_argument('--milvus_database', type=str, required=False, default=None,
                        help='Path to the Milvus databse.')
    parser.add_argument('--mongodb_database', type=str, required=False, default=None,
                        help='Path to the MongoDB database.')
    parser.add_argument('--load_csv', action='store_true',
                        help='Flag to enable loading images from CSV.')
    parser.add_argument('--load_img_root_path', type=str, required=False, default=None,
                        help='Root path for loading images.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_arguments()
    #TODO implement build databases
    build_databases(args.milvus_database, arg.mongodb_database)
    if args.load_csv is not None:
        load_data(args.load_csv, args.load_img_root_path)
    uvicorn.run(app=app, host='0.0.0.0', port=5000)
