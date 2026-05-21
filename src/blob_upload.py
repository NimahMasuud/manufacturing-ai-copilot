from azure.storage.blob import BlobServiceClient
from src.config import STORAGE_CONN_STRING, CONTAINER_NAME
import os

def upload_csvs(data_folder="data"):
    client = BlobServiceClient.from_connection_string(STORAGE_CONN_STRING)
    container = client.get_container_client(CONTAINER_NAME)

    try:
        container.create_container()
        print(f"Container '{CONTAINER_NAME}' created.")
    except Exception:
        print(f"Container '{CONTAINER_NAME}' already exists.")

    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, "rb") as data:
                container.upload_blob(name=filename, data=data, overwrite=True)
            print(f"Uploaded: {filename}")