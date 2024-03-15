import sqlite3
import json
from .views_helper import dict_factory
from datetime import datetime

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
                u.id AS user_id,
                p.id AS post_number,
                p.user_id AS post_author,
                p.title AS post_title,
                p.image_url,
                p.publication_date,
                p.content AS post_content,
                p.approved,
                p.category_id
            FROM Comments C
            JOIN Users u
                on u.id = c.author_id
            JOIN Posts p
                on p.id = c.post_id
        """
        )

        query_results = db_cursor.fetchall()

        comments = []

        for row in query_results:
            post = {
                "id": row["post_number"],
                "title": row["post_title"],
                "image_url": row["image_url"],
                "publication_date": row["publication_date"],
                "content": row["post_content"],
                "approved": row["approved"],
                "user_id": row["post_author"],
                "category_id": row["category_id"],
            }
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
                "post": post,
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
                datetime.now(),
            ),
        )
        rows_affected = db_cursor.rowcount
    return True if rows_affected > 0 else False
