import requests
from PIL import Image
from io import BytesIO

def download_image_from_drive_url(drive_url: str):
    try:
        # Extract file ID from URL
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[-1]
        elif "/d/" in drive_url:
            file_id = drive_url.split("/d/")[1].split("/")[0]
        else:
            print("Invalid Google Drive URL format")
            return None

        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(direct_url)
        response.raise_for_status()

        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Failed to download image: {e}")
        return None
