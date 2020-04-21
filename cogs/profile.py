import discord
from discord.ext import commands
import utils
import asyncio

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # copies the senders message to the specified channel
    @commands.command()
    async def createprofile(self, ctx):
        def dm_check(m):
            return m.channel.type == discord.channel.ChannelType.private and m.author == ctx.author

        await ctx.author.send("What is your villager's name?")
        try:
            await self.bot.wait_for('message', check = dm_check, timeout = 10.0)
        except asyncio.TimeoutError:
            await ctx.author.send("The message timed out")
        else:
            await ctx.author.send("You replied to the message")


def setup(bot):
    bot.add_cog(Profile(bot))
