import requests

def upload_file_to_ipfs(file):
    """
    Uploads a file to IPFS via the local Kubo HTTP API.

    Args:
        file: Django UploadedFile or file-like object

    Returns:
        str: CID of the uploaded file
    """
    try:
        file.seek(0)  # Ensure file pointer is at start
        files = {'file': (file.name, file)}
        response = requests.post('http://127.0.0.1:5001/api/v0/add', files=files)
        response.raise_for_status()
        return response.json()['Hash']
    except Exception as e:
        print(f"IPFS upload error: {e}")
        return None
