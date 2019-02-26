import requests
import json
import urllib
import os
import zipfile

branch = os.environ["BITRISE_GIT_BRANCH"]
buildType = 'snapshot'
if branch == 'master':
    buildType = 'release'

response = requests.get('https://api.github.com/repos/'+os.environ["REPOSITORY_NAME"]+'/releases', headers={'Authorization': 'token '+ os.environ["GITHUB_API_TOKEN"]})
releases = json.loads(response.text)

assetUrl = ""
for release in releases:
    print (release)
    if buildType in release['tag_name']:
        print (release['tag_name'])
        assetUrl = release['assets'][0]['url']
        break

with requests.get(assetUrl+'?access_token='+os.environ["GITHUB_API_TOKEN"],headers={'Accept': 'application/octet-stream'}) as r:
    with open("last_release.zip", 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

with zipfile.ZipFile("last_release.zip","r") as zip_ref:
    zip_ref.extractall()

deployFiles = os.listdir('./deploy')
for filename in os.listdir('./deploy'):
    if filename.endswith('.apk'):
        os.rename('./deploy/'+filename, './deploy/old.apk')
