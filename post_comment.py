import json
import requests
import os
from itertools import islice

user = os.environ["CIRCLE_PROJECT_USERNAME"]
project = os.environ["CIRCLE_PROJECT_REPONAME"]
pr_url = os.environ["CIRCLE_PULL_REQUEST"]
pr_no = pr_url[len(pr_url)-1]
print(pr_no)
body = ""
with open("apkDiff.txt") as apk_diff:
    for line in islice(apk_diff, 5):
        body += line

payload = {
    'body': body
}
response = requests.post('https://api.github.com/repos/' + user + '/' + project + '/issues/' + pr_no + '/comments',
                         data=json.dumps(payload),
                         headers={'Authorization': 'token '+ os.environ["GITHUB_API_TOKEN"]})
