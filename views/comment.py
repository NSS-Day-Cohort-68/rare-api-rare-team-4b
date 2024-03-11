import sqlite3
import json
from .views_helper import dict_factory

database = "./db.sqlite3"

def get_comments():

    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT *
            FROM Comments
        """
        )

        query_results = db_cursor.fetchall()

        comments = []

        for row in query_results:
            comment = {
                "id": row['id'],
                "post_id": row['post_id'],
                "author_id": row['author_id'],
                "content": row['content']
            }
            comments.append(comment)
        serialized_comments = json.dumps(comments)
    return serialized_comments


def get_single_comment(pk):
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
        """
            SELECT
                c.id,
                c.post_id,
                c.author_id,
                c.content
            FROM Comments c
            WHERE c.id = ?
        """,(pk,))
        query_results = db_cursor.fetchone()

        dictionary_version_of_object = dict(query_results)
        serialized_comment = json.dumps(dictionary_version_of_object)
    return serialized_comment