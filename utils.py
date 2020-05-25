list_of_developers = {
    "Plugs": 146737110974595073,
    "RedVelvetUnderground": 449997098956488724
}


# search formatting
def format_input(input):
    str_input = "".join(input) # join arguments together
    # fix casing
    word_list = str_input.lower().split(" ") # split each word by space and make lowercase
    output = []
    for word in word_list:
        output.append(word.capitalize()) # capitalise all lowercase words in list
    return " ".join(output) # join words back together with a space between them


# check if a developer is using the command
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
