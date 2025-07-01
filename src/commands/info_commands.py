import discord
from discord.ext import commands

async def info(ctx: commands.Context):
    """Show bot information."""
    embed = discord.Embed(
        title="Music Bot Information",
        description="This bot is a minimal music player for Discord.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Version", value="1.0.0", inline=True)
    embed.add_field(name="Author", value="Jonas", inline=True)
    embed.add_field(name="GitHub", value="[Repository]()", inline=True)
    await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    """Register the !info command with the bot."""
    bot.add_command(commands.Command(info, name="info", aliases=["about"], help="Show bot information"))

