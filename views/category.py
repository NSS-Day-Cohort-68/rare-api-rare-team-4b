import sqlite3
import json
from datetime import datetime
from .views_helper import dict_factory


database = "./db.sqlite3"


def create_category(category_data):
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Categories (label)
            VALUES (?)
            """,
            (category_data["label"],)
        )

        # Get the last inserted row id to confirm the creation
        new_category_id = db_cursor.lastrowid

    return new_category_id


def list_categories(url):
    expand_param = url["query_params"].get("_expand")
    # Open a connection to the database
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
                """
            SELECT
                c.id,
                c.label
            FROM Categories c              
            """
            )
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it

        categories = []
        for row in query_results:
            category = {
                "id": row['id'],
                "label": row['label']
            }
            categories.append(category)

        # Serialize Python list to JSON encoded string
        serialized_categories = json.dumps(categories)

    return serialized_categories


def retrieve_categories(pk, expand=False):
    # Open a connection to the database
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        if expand:
            # Write the SQL query to get the information you want
            db_cursor.execute(
                """
            SELECT
                c.id,
                c.label
            FROM Categories c
            WHERE c.id = ?
            """,
                (pk,),
            )
        else:
            # Write the SQL query to get the information without expansion
            db_cursor.execute(
                """
            SELECT
                c.id,
                c.label
            FROM Categories c
            WHERE c.id = ?
            """,
                (pk,),
            )

        query_results = db_cursor.fetchone()

        if not query_results:
            return None  # Return None if category is not found

        # Convert the sqlite3.Row object to a dictionary
        query_results_dict = dict(query_results)

        category = {
            "id": query_results_dict["id"],
            "label": query_results_dict["label"],
        }

        if expand:
            category["category_id"] = query_results_dict.get("category_id")
            category["category"] = (
                {
                    "id": query_results_dict.get("category_id"),
                    "label": query_results_dict.get("category_label"),
                }
                if expand
                else None
            )
        # Serialize Python list to JSON encoded string

        serialized_category = json.dumps(category)

    return serialized_category
