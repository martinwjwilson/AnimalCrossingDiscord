# TODO: Remove this and add proper database queries
# https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
def double_apostrophes(text):
    new_text = ""
    for letter in text:
        if letter == "'":
            new_text += "'"
        new_text += letter
    return new_text


# SQL STATEMENTS

QUERY_SEARCH_FOR_CRITTER_NAMED = """SELECT *
                FROM critter
                WHERE critter_name = ?"""


QUERY_SEARCH_ALL_CRITTERS = """SELECT *
                FROM critter
                WHERE species = ?
                ORDER BY critter_name ASC"""

QUERY_SEARCH_ALL_CRITTERS_STARTING_WITH = """SELECT *
                FROM critter
                WHERE species = ?
                AND critter_name LIKE ?
                ORDER BY critter_name ASC"""
