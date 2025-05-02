import sqlite3
import disnake
from disnake.ext import commands
import asyncio

# db
conn = sqlite3.connect("critterpedia.db")
c = conn.cursor()


class Profile(commands.Cog):
    @staticmethod
    def create_profile():
        # obtain the user information
        villager_name = input("What is your villager's name?")
        island_name = input("What is your island's name?\n")
        friend_code = input("What is your friend code?\n"
                            "Please type `no` if you do not wish to provide this\n")
        print(villager_name)
        print(island_name)
        print(friend_code)
