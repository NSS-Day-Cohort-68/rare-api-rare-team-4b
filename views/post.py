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
            """
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            user = {
                "id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "username": row["username"],
                "email": row["email"],
            }
            category = {
                "id": row["category_id"],
                "label": row["label"],
            }
            post = {
                "id": row["id"],
                "title": row["title"],
                "image_url": row["image_url"],
                "publication_date": row["publication_date"],
                "content": row["content"],
                "approved": row["approved"],
                "user_id": row["user_id"],
                "user": user,
                "category_id": row["category_id"],
                "category": category,
            }

            posts.append(post)

    return json.dumps(posts)


def create_post(user_id, category_id, title, content, image_url=None):
    """
    Creates a new post in the database.

    Returns:
        bool: True if the post was created successfully, False otherwise.
    """
    publication_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    approved = 1  # Assuming 1 for true/approved

    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Posts (user_id, category_id, title, content, image_url, publication_date, approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                category_id,
                title,
                content,
                image_url,
                publication_date,
                approved,
            ),
        )
        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False
