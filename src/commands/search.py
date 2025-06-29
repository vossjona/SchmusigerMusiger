import discord
from discord.ext import commands


async def search(ctx: commands.Context, query: str):
    """Search for a song using the provided query."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def search_youtube(ctx: commands.Context, query: str):
    """Search for a song on YouTube using the provided query."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def search_soundcloud(ctx: commands.Context, query: str):
    """Search for a song on SoundCloud using the provided query."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def search_spotify(ctx: commands.Context, query: str):
    """Search for a song on Spotify using the provided query."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def song_info(ctx: commands.Context, url: str):
    """Show information about a specific song."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_command(commands.Command(search, name="search", help="Search for a song"))
    bot.add_command(commands.Command(search_youtube, name="search_youtube", help="Search for a song on YouTube"))
    bot.add_command(commands.Command(search_soundcloud, name="search_soundcloud", help="Search for a song on SoundCloud"))
    bot.add_command(commands.Command(search_spotify, name="search_spotify", help="Search for a song on Spotify"))
    bot.add_command(commands.Command(song_info, name="song_info", help="Show information about a specific song"))


