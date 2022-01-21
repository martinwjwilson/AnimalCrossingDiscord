import disnake
from disnake.ext import commands
import utils


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # copies the senders message to the specified channel
    @commands.command(hidden=True)
    @commands.check(utils.check_if_it_is_dev)
    async def echo(self, ctx, channel: disnake.TextChannel, *, words):
        await ctx.message.delete()
        await channel.send(words)


def setup(bot):
    bot.add_cog(Admin(bot))
