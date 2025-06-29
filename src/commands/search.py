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