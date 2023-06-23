import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


def upload_to_mp3s_container(name_of_mp3):
    connect_str = 'DefaultEndpointsProtocol=https;AccountName=popouteventsblob;AccountKey=6aklcEq/gWu/CXiaopvaDHQtQb3oTdkMLmVMBFG2xEo4OCN+QlLiBKt8OT4v1e1SE4ZItBcwt/rj+ASttqIV1g==;EndpointSuffix=core.windows.net'

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    # container_name = str(uuid.uuid4())

    # Create the container
    # container_client = blob_service_client.get_container_client(container = "mp3s")

    local_file_name = name_of_mp3

    # Create a local directory to hold blob data
    print("after")
    local_path = "../routes/mp3s"
    print("before")
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create a file in the local data directory to upload and download

    upload_file_path = os.path.join(script_dir,os.path.join(local_path, local_file_name))

    # Write text to the file
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container="mp3s", blob=local_file_name)
    # print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True,
                                content_type="audio/mpeg")
    return "https://cdn.popout.gr/mp3s/"+name_of_mp3
