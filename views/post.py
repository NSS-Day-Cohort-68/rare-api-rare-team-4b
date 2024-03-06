import sqlite3
import json
from datetime import datetime
from .views_helper import dict_factory

database = "./db.sqlite3"


def specific_post(pk):
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
                SELECT
                    p.id,
                    p.title,
                    p.content,
                    p.publication_date,
                    u.username
                FROM Posts p
                JOIN Users u
                    ON u.id = p.user_id
                WHERE p.id = ?
                    """,
            (pk,),
        )

    query_results = db_cursor.fetchone()
    return json.dumps(query_results) if query_results else None


def get_all_posts():
    """Retrieves all the posts from the database

    Returns:
        json string: A JSON string with all posts
    """

    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT *
            FROM Posts
        """
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = {
                "id": row["id"],
                "user_id": row["user_id"],
                "category-id": row["category_id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
            }
            posts.append(post)
        serialized_posts = json.dumps(posts)
    return serialized_posts
