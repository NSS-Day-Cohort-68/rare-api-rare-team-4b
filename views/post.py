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
                p.user_id,
                p.category_id,
                p.title,
                p.image_url,
                p.publication_date,
                p.content,
                p.approved,
                u.first_name,
                u.last_name,
                u.username,
                u.email,
                c.label
            FROM Posts p
            JOIN Users u
                ON u.id = p.user_id
            JOIN Categories c
                ON c.id = p.category_id
            WHERE p.id = ?
            """,
            (pk,),
        )

        query_results = db_cursor.fetchone()
        if query_results:
            user = {
                "id": query_results["user_id"],
                "first_name": query_results["first_name"],
                "last_name": query_results["last_name"],
                "username": query_results["username"],
                "email": query_results["email"],
            }
            category = {
                "id": query_results["category_id"],
                "label": query_results["label"],
            }
            post = {
                "id": query_results["id"],
                "title": query_results["title"],
                "image_url": query_results["image_url"],
                "publication_date": query_results["publication_date"],
                "content": query_results["content"],
                "approved": query_results["approved"],
                "user_id": query_results["user_id"],
                "user": user,
                "category_id": query_results["category_id"],
                "category": category,
            }
            return json.dumps(post)

    return None


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
                "category_id": row["category_id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "image_url": row["image_url"],
                "content": row["content"],
                "approved": row["approved"],
            }
            posts.append(post)
        serialized_posts = json.dumps(posts)
    return serialized_posts
