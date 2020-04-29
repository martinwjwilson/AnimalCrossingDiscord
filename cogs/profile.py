import discord
from discord.ext import commands
import utils
import asyncio

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # ask a user for their name
    async def get_info(self, ctx, question):
        def dm_check(m):
            return m.channel.type == discord.channel.ChannelType.private and m.author == ctx.author
        await ctx.author.send(question) # send the user a dm
        try:
            recieved_message = await self.bot.wait_for('message', check = dm_check, timeout = 10.0) # wait for a response
            message_content = recieved_message.content
        except asyncio.TimeoutError:
            await ctx.author.send("The message timed out") # if they do not respond
        else:
            return message_content

    # create a profile for the user
    @commands.command()
    async def createprofile(self, ctx):
        # obtain the user information
        villager_name = await self.get_info(ctx, "What is your villager's name?")
        print(villager_name)
        # discord_name =
        island_name = await self.get_info(ctx, "What is your island's name?")
        print(island_name)
        # friend_code =

def setup(bot):
    bot.add_cog(Profile(bot))
