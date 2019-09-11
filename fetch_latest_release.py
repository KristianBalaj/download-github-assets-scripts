##################################################
## Author: Kristian Balaj
## License: MIT
## Email: kiko.balaj@gmail.com
##################################################
import requests
import json
import sys

# https://developer.github.com/v3/repos/releases/#get-the-latest-release

if len(sys.argv) == 1 or sys.argv[1] == '--help' or len(sys.argv) not in (3, 4):
    print("usage: fetch_latest_release.py [--help] owner repo [token]")
    print("")
    print("Downloads the latest release of the repo from GitHub and stores the binary in the current directory.")
    print("")
    print("positional arguments:")
    print("owner       owner of the repository")
    print("repo        repository name")
    print("")
    print("optional positional arguments:")
    print("--help       prints script manual")
    print("token       authentication token (used for private repos)")
    sys.exit()

owner = sys.argv[1]  # e.g. KristianBalaj
repo = sys.argv[2]  # e.g. download-github-assets-scripts
url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
headers = { 
    'Accept': 'application/json'
}

if len(sys.argv) > 3:
    token = sys.argv[3]  # e.g. 4396ee4b4....
    headers['Authorization'] = f"token {token}"

response = requests.get(url=url, headers=headers)

if response.status_code == 200:
    json_result = json.loads(response.content)
    try:
        download_url = json_result['assets'][0]['url']
        asset_name = json_result['assets'][0]['name']
    except (KeyError, IndexError):
        print("Cannot get the latest release. Does the release exist?")
        sys.exit()
    headers['Accept'] = 'application/octet-stream'
    response_download = requests.get(url=download_url, headers=headers)
    if response_download.status_code == 200:
        with open(f"./{asset_name}", 'wb') as f:
            f.write(response_download.content)
        print(f"Download stored as ./{asset_name}")
    else:
        print(f"Didn't get download success. Status code {response_download.status_code}")
else:
    print(f"Didn't get the latest release info. Status code {response.status_code}")
