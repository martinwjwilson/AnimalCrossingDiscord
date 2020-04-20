import discord
from discord.ext import commands
import utils
import asyncio

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # def check(message):
    #     return message.channel.type == discord.ChannelType.private

    async def pred(self, ctx):
        print(f"The channel type was: {m.message.channel.type}")
        return m.message.channel.type == discord.ChannelType.private

    # copies the senders message to the specified channel
    @commands.command()
    async def createprofile(self, ctx):
        # await ctx.message.author.send("What is your villager's name?")
        # await self.bot.wait_for('message', check = check())
        try:
            msg = await self.bot.wait_for('message', check=self.pred(ctx), timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.message.author.send('You took too long...')
        else:
            await ctx.message.author.send('You said {0.content}, {0.author}.'.format(msg))




def setup(bot):
    bot.add_cog(Profile(bot))
