# check if a developer is using the command
list_of_developers = {
"Plugs": 146737110974595073,
"RedVelvetUnderground": 449997098956488724
}

def check_if_it_is_dev(ctx):
    if ctx.message.author.id in list_of_developers.values():
        return True


# SQL STATEMENTS
def check_for_critter(name):
    return f"""SELECT *
                FROM critter
                WHERE critter_name = '{name}'"""

def search_all_critters(type, starts_with):
    return f"""SELECT *
                FROM critter
                WHERE species = '{type}'
                {starts_with}
                ORDER BY critter_name ASC"""

# def create_new_profile(villager_name, island_name, friend_code):
#     return f"""INSERT INTO """
