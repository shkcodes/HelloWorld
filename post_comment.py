import json
import requests
import os
from itertools import islice
from tabulate import tabulate

user = os.environ["CIRCLE_PROJECT_USERNAME"]
project = os.environ["CIRCLE_PROJECT_REPONAME"]
pr_url = os.environ["CIRCLE_PULL_REQUEST"]
pr_no = pr_url[pr_url.rfind('/') + 1:]
body = ""
lines = open("apkDiff.txt", "r").read().splitlines()
byteToMBMultiplier = float(1) / (1024 * 1024)
decimalFormatter = '{0:+.3f}'

classesDexSize = 0
resSize = 0
layoutSize = 0

re.split('\t', lines[0])

for line in lines:
    tabs = re.split('\t', line)
    if "classes" in tabs[3]:
        classesDexSize += float(tabs[2])
    if "/res/" in tabs[3]:
        resSize += float(tabs[2])
    if "/res/layout/" in tabs[3]:
        layoutSize += float(tabs[2])

classesDexSize = str(decimalFormatter.format(classesDexSize * byteToMBMultiplier))
resSize = str(decimalFormatter.format(resSize * byteToMBMultiplier))
layoutSize = str(decimalFormatter.format(layoutSize * byteToMBMultiplier))
apkSize = str(decimalFormatter.format(float(re.split('\t', lines[0])[2]) * byteToMBMultiplier))

body = tabulate([["apk size", apkSize + "MB"],
                ["dex size", classesDexSize + "MB"],
                ["res size", resSize + "MB"],
                ["layout size", layoutSize + "MB"]],
               tablefmt="grid")
payload = {
    'body': body
}
response = requests.post('https://api.github.com/repos/' + user + '/' + project + '/issues/' + pr_no + '/comments',
                         data=json.dumps(payload),
                         headers={'Authorization': 'token '+ os.environ["GITHUB_API_TOKEN"]})
