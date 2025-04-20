# check if a developer is using the command
list_of_developers = {
    "Plugs": 146737110974595073,
    "RedVelvetUnderground": 449997098956488724
}


def check_if_it_is_dev(ctx):
    if ctx.message.author.id in list_of_developers.values():
        return True


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


def search_all_critters(type, starts_with):
    return f"""SELECT *
                FROM critter
                WHERE species = '{type}'
                {starts_with}
                ORDER BY critter_name ASC"""

# def create_new_profile(villager_name, island_name, friend_code):
#     return f"""INSERT INTO """
