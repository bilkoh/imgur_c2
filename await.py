import requests
import json
import os
import sqlite3 as sl
from imgur_c2.auth import client_id

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "imgur-history.db")
con = None


def init_db(db_path=SQLITE_PATH):
    global con
    con = sl.connect(db_path)

    with con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS IMGUR_HISTORY (
                id INTEGER PRIMARY KEY,
                imgur_id TEXT,
                last_exec TEXT
            );
            """
        )


def get_images_by_tag(tag):
    url = (
        "https://api.imgur.com/post/v1/posts/t/"
        + tag
        + "?client_id="
        + client_id
        + "&filter%5Bwindow%5D=week&include=adtiles%2Cadconfig%2Ccover&page=1&sort=-viral"
    )
    res = requests.get(url).content
    data = json.loads(res)
    images = []

    if "errors" in data:
        print("Errors:", data["errors"])
    elif "posts" in data:
        # print(json.dumps(data["posts"], indent=2))
        for i in data["posts"]:
            images.append(i["id"])
    else:
        print("Unknown Error:", data)

    # to download an image w/ ID use https://imgur.com/download/53i9bwZ/imgur_upload

    return images


def is_in_history(imgur_id):
    global con
    if con is None:
        init_db()

    with con:
        cur = con.cursor()
        sql = "SELECT * FROM IMGUR_HISTORY WHERE imgur_id=?;"
        cur.execute(sql, (imgur_id,))
        return cur.fetchone()


def execute_by_imgur_id(imgur_id):
    global con
    if con is None:
        init_db()

    # execution stuff from ImgMsg module here

    # if successfully executed
    with con:
        cur = con.cursor()
        sql = "INSERT INTO IMGUR_HISTORY (imgur_id, last_exec) VALUES (?, datetime('now'));"
        cur.execute(sql, (imgur_id,))


for i in get_images_by_tag("a8a15930df81"):
    print(i)
    # execute_by_imgur_id(i)
    print(is_in_history(i))
