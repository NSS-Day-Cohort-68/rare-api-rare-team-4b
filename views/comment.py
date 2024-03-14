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
            SELECT 
                c.id AS comment_id,
                c.post_id,
                c.author_id,
                c.content,
                c.date,
                u.first_name,
                u.last_name,
                u.username,
                u.email,
                u.id AS user_id
            FROM Comments C
            JOIN Users u
                on u.id = c.author_id
        """
        )

        query_results = db_cursor.fetchall()

        comments = []

        for row in query_results:
            user = {
                "id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "username": row["username"],
                "email": row["email"],
            }
            comment = {
                "id": row["comment_id"],
                "post_id": row["post_id"],
                "author_id": row["author_id"],
                "content": row["content"],
                "date": row["date"],
                "user": user,
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
                c.content,
                c.date

            FROM Comments c
            WHERE c.id = ?
        """,
            (pk,),
        )
        query_results = db_cursor.fetchone()

        dictionary_version_of_object = dict(query_results)
        serialized_comment = json.dumps(dictionary_version_of_object)
    return serialized_comment


def add_comment(data):
    with sqlite3.connect(database) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                INSERT INTO Comments (post_id, author_id, content, date)
                VALUES (?,?,?,?)
            """,
            (
                data["post_id"],
                data["author_id"],
                data["content"],
                data["date"],
            ),
        )
        rows_affected = db_cursor.rowcount
    return True if rows_affected > 0 else False
