import os
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import sys


def upload_to_event_image_container(name_of_image):
    connect_str = 'DefaultEndpointsProtocol=https;AccountName=popouteventsblob;AccountKey=6aklcEq/gWu/CXiaopvaDHQtQb3oTdkMLmVMBFG2xEo4OCN+QlLiBKt8OT4v1e1SE4ZItBcwt/rj+ASttqIV1g==;EndpointSuffix=core.windows.net'
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    # container_name = str(uuid.uuid4())

    # Create the container
    # container_client = blob_service_client.get_container_client(container = "mp3s")

    # Create a local directory to hold blob data
    full_path = "../images/"+name_of_image

    # Create a file in the local data directory to upload and download

    # Write text to the file
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container="eventsimages", blob=name_of_image)
    # print("\nUploading to Azure Storage as blob:\n\t" + name_of_image)
    # Upload the created file
    with open(full_path, "rb") as data:
        res = blob_client.upload_blob(
            data, overwrite=True, content_type="image/webp")

    return "https://cdn.popout.gr/eventsimages/"+name_of_image
