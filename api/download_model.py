import requests
import zipfile

DOWNLOAD_LINK = (
    "https://api.onedrive.com/v1.0/shares/u!"
    + "aHR0cHM6Ly8xZHJ2Lm1zL3UvcyFBalpDaVlrY2twdF9oWXg4UF8zUEFoeG1udjNtdEE"
    + "/root/content"
)


def download_model():
    """Download trained spaCy model"""
    with requests.get(DOWNLOAD_LINK, stream=True) as r:
        r.raise_for_status()
        with open("model-best.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile("model-best.zip", "r") as f:
        f.extractall()
