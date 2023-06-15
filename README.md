# zilliz-mongodb-demo

## Introduction 
This is a demo project that showcases the integration of Milvus and MongoDB for an e-commerce platform. It allows searching for similar images and texts based on uploaded content. The project is built using FastAPI and provides an API for performing these search operations.

## Prerequisites
Before running the demo, make sure you have the following dependencies installed:
 - Milvus: Install and configure Milvus by following the official documentation.
 - MongoDB: Install and configure MongoDB by following the official documentation.

## Getting Started
To get started with the demo, follow the steps below:
 1. Clone the repository and navigate to the project directory.
 2. Install the required Python packages by running pip install -r requirements.txt.
 3. Prepare the dataset #TODO
 4. Start the server
    ```bash
    python main.py --csv --root --num --purge 
    ```
## API Endpoints

### Image Search
**Endpoint:** `POST /img/seach`

This endpoint allows you to search for similar images based on an uploaded image.

**Request Parameters:**
 - `image` (file): The image file to search.
 - `topk` (int): The number of similar images to retrieve.
 - `table_name` (str): The name of the table in Milvus.

**Example Request:**      
 ```bash
    curl -X POST -F "image=@image.jpg" -F "topk=5" -F "table_name=my_table" http://localhost:5000/img/search
 ```

### Text Search
**Endpoint:** `POST /text/seach`

This endpoint allows you to search for similar texts based on a provided text query.

**Request Parameters:**
 - `text` (str): The text query to search.
 - `topk` (int): The number of similar texts to retrieve.
 - `table_name` (str): The name of the table in Milvus.

**Example Request:**      
 ```bash
    curl -X POST -F "text=example text" -F "topk=5" -F "table_name=my_table" http://localhost:5000/text/search
 ```

### Image Upload 
**Endpoint:** `POST /image/upload`

This endpoint allows you to upload an image to the server for indexing and searching.

**Request Parameters:**
 - `image` (file): The text query to search.
 - `url` (int): The number of similar texts to retrieve.
 - `meta_info` (dict): The extra meta information of uploaded item. 
 - `table_name` (str): The name of the table in Milvus.

**Example Request:**      
 ```bash
    curl -X POST -F "image=@image.jpg" -F "table_name=my_table" http://localhost:5000/img/upload
 ```





