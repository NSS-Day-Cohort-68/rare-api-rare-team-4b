import sqlite3
import json
from .views_helper import dict_factory
from datetime import datetime

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
