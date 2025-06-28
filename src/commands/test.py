from discord.ext import commands

async def test_cmd(ctx: commands.Context):
    """Responds to !test with a placeholder message."""
    await ctx.send("Test command is working!")


def setup(bot: commands.Bot):
    bot.add_command(commands.Command(test_cmd, name="test"))