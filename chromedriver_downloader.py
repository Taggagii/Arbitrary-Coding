import requests
import zipfile
from io import BytesIO

def download_chrome_driver(version = None):
    try:
        version_number = ""
        if version:
            version_number = "_" + version
        latest_release = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE{version_number}").content.decode("utf-8")
        
        zip_file_page_ref = requests.get(f"https://chromedriver.storage.googleapis.com/{latest_release}/chromedriver_win32.zip")
        zip_file_bytes_io = BytesIO(zip_file_page_ref.content)
        zip_file = zipfile.ZipFile(zip_file_bytes_io)
        zip_file.extractall()
        return 1
    except:
        return 0
