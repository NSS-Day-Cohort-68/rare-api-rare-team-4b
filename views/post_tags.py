import sqlite3
import json
from .views_helper import dict_factory

database = "./db.sqlite3"


def get_post_tags():
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                pt.id,
                pt.post_id,
                pt.tag_id,
                t.label,
                FROM PostTags pt,
                JOIN Tags t
                    ON t.id = pt.tag_id
             """
        )
        query_results = db_cursor.fetchall()

        post_tags = []
        for row in query_results:
            post_tag = {
                "post_tag_id": row["id"],
                "post_id": row["post_id"],
                "tag_id": row["tag_id"],
                "tag": {
                    "id": row["tag_id"],
                    "label": row["label"],
                },
            }

            post_tags.append(post_tag)
    return json.dumps(post_tags)
