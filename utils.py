# check if a developer is using the command
list_of_developers = {
"Plugs": 146737110974595073,
"RedVelvetUnderground": 449997098956488724
}

def check_if_it_is_dev(ctx):
    if ctx.message.author.id in list_of_developers.values():
        return True


# SQL STATEMENTS
def check_for_critter(type, name):
    return f"""SELECT *
                FROM {type}
                WHERE name = '{name}'"""

def search_all_critters(type, starts_with):
    return f"""SELECT *
                FROM {type}
                {starts_with}
                ORDER BY name ASC"""

# def create_new_profile(villager_name, island_name, friend_code):
#     return f"""INSERT INTO """
