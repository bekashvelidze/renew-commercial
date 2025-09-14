import json
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import requests


def local_version():
    with open("version.json", "r") as file:
        data = json.load(file)

    return data["version"]

def read_online():
    url = "https://github.com/bekashvelidze/renew-commercial/raw/main/version.json"
    resp = requests.get(url)
    data = json.loads(resp.text)
    version_info = data["version"]

    return version_info


version = read_online()
version_local = local_version()
extract_to = "."

print(version, version_local)
if version == version_local:
    print("An application is already up to date.")
else:
    print(f"You have outdated version of applicatin {version_local} An update for application is available.")
    file_to_download = "https://github.com/bekashvelidze/renew-commercial/archive/refs/heads/main.zip"
    http_response = urlopen(file_to_download)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


if __name__ == "__main__":
    local_version()