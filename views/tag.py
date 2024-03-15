import sqlite3
import json
from .views_helper import dict_factory

database = "./db.sqlite3"


def get_tag(pk):
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                t.id,
                t.label
            FROM Tags t
            WHERE t.id = ?
            """,
            (pk,),
        )

        query_results = db_cursor.fetchone()

    return json.dumps(query_results) if query_results else None


def get_all_tags():
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                t.id,
                t.label
            FROM Tags t
            """
        )
        query_results = db_cursor.fetchall()

        tags = []
        for row in query_results:
            tags.append(row)

    return json.dumps(tags)


def delete_tag(pk):
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Tags
            WHERE id = ?
            """,
            (pk,),
        )

    return True if db_cursor.rowcount > 0 else False
