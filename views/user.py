import sqlite3
import json
from datetime import datetime
from .views_helper import dict_factory

database = "./db.sqlite3"


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and email of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect(database) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and email = ?
            """,
            (user["username"], user["email"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect(database) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Users (first_name, last_name, username, email, password, bio, created_on, profile_image_url, active) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
                user.get("profile_image_url", ""),
                user.get("active", 1),
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_user(pk):
    """Retrieves one user from the database

    Args:
        pk (int): The primary key of the user to retrieve

    Returns:
        json string: A JSON string containing the user's details if found, otherwise None
    """

    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Users u
            WHERE u.id = ?
            """,
            (pk,),
        )

        query_results = db_cursor.fetchone()

    return json.dumps(query_results) if query_results else None


def get_all_users():
    """Retrieves all users from the database

    Returns:
        json string: A JSON string containing all user records
    """

    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.bio,
                u.username,
                u.password,
                u.profile_image_url,
                u.created_on,
                u.active
            FROM Users u
            """
        )
        query_results = db_cursor.fetchall()

        users = []
        for row in query_results:
            users.append(row)

    return json.dumps(users)


def create_tag(tag):
    print("Tag received:", tag)  # Print statement to see the content of the tag
    with sqlite3.connect(database) as conn:
        conn.row_factory = dict_factory
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Tags (label)
            VALUES (?)
            """,
            (tag["label"],),
        )

        # Get the last inserted row to confirm the creation
        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False
