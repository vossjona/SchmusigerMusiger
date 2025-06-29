import discord
from discord.ext import commands

async def queue(ctx: commands.Context):
    """Show the current playback queue."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def now_playing(ctx: commands.Context):
    """Show the currently playing track."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def clear_queue(ctx: commands.Context):
    """Clear the current playback queue."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def skip(ctx: commands.Context):
    """Skip the current track."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def skip_n(ctx: commands.Context, n: int):
    """Skip the next N tracks in the queue."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def remove_n(ctx: commands.Context, n: int):
    """Remove the Nth track from the queue."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


async def shuffle(ctx: commands.Context):
    """Shuffle the current playback queue."""
    # Todo
    embed = discord.Embed(
        title="Work in Progress",
    )
    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    """Register the !play command with the bot."""
    bot.add_command(commands.Command(queue, name="queue", help="Show the current playback queue"))
    bot.add_command(commands.Command(now_playing, name="now_playing", help="Show the currently playing track"))
    bot.add_command(commands.Command(clear_queue, name="clear_queue", help="Clear the current playback queue"))
    bot.add_command(commands.Command(skip, name="skip", help="Skip the current track"))
    bot.add_command(commands.Command(skip_n, name="skip_n", help="Skip the next N tracks in the queue"))
    bot.add_command(commands.Command(remove_n, name="remove_n", help="Remove the Nth track from the queue"))
    bot.add_command(commands.Command(shuffle, name="shuffle", help="Shuffle the current playback queue"))