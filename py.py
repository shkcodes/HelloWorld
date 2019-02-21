import requests
import json
import urllib
import os

response = requests.get('https://api.github.com/repos/shkcodes/HelloWorld/releases/latest', headers={'Authorization': 'token '+ os.environ["GITHUB_API_TOKEN"]})
print(os.environ["GITHUB_API_TOKEN"])
model = json.loads(response.text)
downloadUrl = model["assets"][0]["browser_download_url"]
urllib.urlretrieve(downloadUrl, "old.apk")
print(downloadUrl)