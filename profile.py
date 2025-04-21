import sqlite3
import disnake
from disnake.ext import commands
import asyncio

# db
conn = sqlite3.connect("critterpedia.db")
c = conn.cursor()


class Profile(commands.Cog):
    # ask a user for their name
    async def get_info(self, ctx, question):
        def dm_check(m):  # check that the message was a DM from the correct user
            return m.channel.type == disnake.ChannelType.private and m.author == ctx.author

        await ctx.author.send(question)  # send the user a dm
        try:
            received_message = await self.bot.wait_for('message', check=dm_check, timeout=10.0)  # wait for a response
            message_content = received_message.content
        except asyncio.TimeoutError:  # if they do not respond
            await ctx.author.send("The message timed out")
        else:  # if there was no exception
            return message_content

    # create a new DB entry for the user profile
    # async def new_profile(villager_name, island_name, friend_code):

    # create a profile for the user
    def create_profile(self, ctx):
        # obtain the user information
        villager_name = await self.get_info(ctx, "What is your villager's name?")
        # discord_name =
        island_name = await self.get_info(ctx, "What is your island's name?")
        friend_code = await self.get_info(ctx, "What is your friend code? Please type `continue` if you do not wish to provide this")
        print(villager_name)
        print(island_name)
        print(friend_code)
