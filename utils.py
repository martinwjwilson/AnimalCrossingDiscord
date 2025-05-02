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
