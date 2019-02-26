import json
import requests
import os
from itertools import islice
import pytablewriter
import re

#pr_no = os.environ["BITRISE_PULL_REQUEST"]
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
    if "classes" in tabs[3] and ".dex" in tabs[3]:
        classesDexSize += float(tabs[2])
    if "/res/" in tabs[3]:
        resSize += float(tabs[2])
    if "/res/layout/" in tabs[3]:
        layoutSize += float(tabs[2])

classesDexSize = str(decimalFormatter.format(classesDexSize * byteToMBMultiplier))
resSize = str(decimalFormatter.format(resSize * byteToMBMultiplier))
layoutSize = str(decimalFormatter.format(layoutSize * byteToMBMultiplier))
apkSize = str(decimalFormatter.format(float(re.split('\t', lines[0])[2]) * byteToMBMultiplier))


writer = pytablewriter.MarkdownTableWriter()
writer.headers = ["", ""]
writer.value_matrix = [["APK SIZE", apkSize + "MB"],
                       ["DEX SIZE", classesDexSize + "MB"],
                       ["RES SIZE", resSize + "MB"],
                       ["LAYOUT SIZE", layoutSize + "MB"]]

body = writer.dumps()
payload = {
    'body': body
}
print(body)
#response = requests.post('https://api.github.com/repos/' + os.environ["REPOSITORY_NAME"] + '/issues/' + pr_no + '/comments',
#                         data=json.dumps(payload),
#                         headers={'Authorization': 'token '+ os.environ["GITHUB_API_TOKEN"]})
