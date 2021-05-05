import requests
import json
from imgur_c2.auth import client_id


url = (
    "https://api.imgur.com/post/v1/posts/t/a8a15930df81?client_id="
    + client_id
    + "&filter%5Bwindow%5D=week&include=adtiles%2Cadconfig%2Ccover&page=1&sort=-viral"
)
res = requests.get(url).content
print(res)
print("=====")
data = json.loads(res)

if "errors" in data:
    print("Errors:", data["errors"])
elif "posts" in data:
    print(json.dumps(data["posts"], indent=2))

    for i in data["posts"]:
        print(i["id"])
else:
    print("Unknown Error:", data)

# to download an image w/ ID use https://imgur.com/download/53i9bwZ/imgur_upload
