from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from config import MILVUS_HOST, MILVUS_PORT, MILVUS_COLLECTION, VECTOR_DIMENSION, METRIC_TYPE, INDEX_TYPE

def set_collection():
    # Connect to Milvus service
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

    if utility.has_collection(MILVUS_COLLECTION):
        return 

    fields = [
        FieldSchema(name='id', dtype=DataType.VARCHAR, description='id of the image', max_length=500, 
                    is_primary=True, auto_id=False),
        FieldSchema(name='path', dtype=DataType.VARCHAR, description='path to the image', max_length=500, 
                    is_primary=False, auto_id=False),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, description='image embedding vectors', dim=VECTOR_DIMENSION)
    ]
    schema = CollectionSchema(fields=fields, description='zilliz mongo demo')
    collection = Collection(name=MILVUS_COLLECTION, schema=schema)

    index_params = {
        'metric_type': METRIC_TYPE,
        'index_type': INDEX_TYPE,
        'params': {"nlist": 2048}
    }
    collection.create_index(field_name='embedding', index_params=index_params)
    print(f'A new Milvus collection created: {MILVUS_COLLECTION}')
