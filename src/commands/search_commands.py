import discord
from discord.ext import commands

from exceptions import HumanError


async def search(ctx: commands.Context, query: str = None):
    """Search for a song using the provided query."""
    try:
        if not query or query.strip() == "":
            raise HumanError("Please provide a search query. Usage: `!search <query>`")
        
        # Todo
        embed = discord.Embed(
            title="Work in Progress",
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title="Human Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def search_youtube(ctx: commands.Context, query: str = None):
    """Search for a song on YouTube using the provided query."""
    try:
        if not query or query.strip() == "":
            raise HumanError("Please provide a search query. Usage: `!search_youtube <query>`")
        
        # Todo
        embed = discord.Embed(
            title="Work in Progress",
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title="Human Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def search_soundcloud(ctx: commands.Context, query: str = None):
    """Search for a song on SoundCloud using the provided query."""
    try:
        if not query or query.strip() == "":
            raise HumanError("Please provide a search query. Usage: `!search_soundcloud <query>`")
        
        # Todo
        embed = discord.Embed(
            title="Work in Progress",
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title="Human Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def search_spotify(ctx: commands.Context, query: str = None):
    """Search for a song on Spotify using the provided query."""
    try:
        if not query or query.strip() == "":
            raise HumanError("Please provide a search query. Usage: `!search_spotify <query>`")
        
        # Todo
        embed = discord.Embed(
            title="Work in Progress",
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title="Human Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def song_info(ctx: commands.Context, url: str = None):
    """Show information about a specific song."""
    try:
        if not url or url.strip() == "":
            raise HumanError("Please provide a song URL. Usage: `!song_info <url>`")
        
        # Todo
        embed = discord.Embed(
            title="Work in Progress",
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title="Human Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_command(commands.Command(search, name="search", help="Search for a song"))
    bot.add_command(commands.Command(search_youtube, name="search_youtube", help="Search for a song on YouTube"))
    bot.add_command(commands.Command(search_soundcloud, name="search_soundcloud", help="Search for a song on SoundCloud"))
    bot.add_command(commands.Command(search_spotify, name="search_spotify", help="Search for a song on Spotify"))
    bot.add_command(commands.Command(song_info, name="song_info", help="Show information about a specific song"))


