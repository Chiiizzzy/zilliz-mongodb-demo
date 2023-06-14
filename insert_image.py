from towhee import pipe, ops
from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, MONGO_URI, MONGO_DB, MONGO_COLLECTION, THRESHOLD, TOP_K, DEVICE


def do_insert(img_path, sku_data):
    init_pipe = (
        pipe.input( 'path', 'sku')
            .map('sku', 'id', lambda x: x['id'])
    )

    sku_pipe = (
        init_pipe.map('sku', '_id', ops.storage.mongo_insert(uri=MONGO_URI, database=MONGO_DB, collection=MONGO_COLLECTION))
    )

    img_pipe = (
        init_pipe.map('path', 'img', ops.image_decode.cv2_rgb())
            .map('img', 'emb', ops.image_text_embedding.clip(model_name='clip_vit_base_patch32', modality='image', device=DEVICE))
            .map('emb', 'emb', ops.towhee.np_normalize())
            .map(('id', 'path', 'emb'), 'pk', ops.ann_insert.milvus_client(
                host=MILVUS_HOST, port=MILVUS_PORT, collection_name=MILVUS_COLLECTION
            ))
    )

    insert_pipe = (
        img_pipe.concat(sku_pipe).output('id')
    )

    return insert_pipe(img_path, sku_data).to_list()
