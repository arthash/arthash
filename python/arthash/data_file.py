import json, requests


def get(file_or_url):
    if file_or_url.startswith('http:') or file_or_url.startswith('https:'):
        data = requests.get(file_or_url).text
    else:
        data = open(file_or_url).read()

    return json.loads(data)
