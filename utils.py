# TODO: Remove this and add proper database queries
def double_apostrophes(text):
    new_text = ""
    for letter in text:
        if letter == "'":
            new_text += "'"
        new_text += letter
    return new_text


# SQL STATEMENTS
def check_for_critter(name):
    new_name = double_apostrophes(name)
    return f"""SELECT *
                FROM critter
                WHERE critter_name = '{new_name}'"""


def search_all_critters(critter_type, starts_with):
    return f"""SELECT *
                FROM critter
                WHERE species = '{critter_type}'
                {starts_with}
                ORDER BY critter_name ASC"""
