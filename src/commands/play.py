import discord
from discord.ext import commands

from audio_manager import play_url, PlaybackError
from youtube import YouTubeMetadata, extract_info


async def play(ctx: commands.Context, url: str):
    """Stream audio from a YouTube URL into the caller's voice channel."""
    # Ensure the author is in a voice channel
    if ctx.author.voice is None:
        embed = discord.Embed(
            title="Voice Channel Required",
            description="You must be connected to a voice channel to use this command.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    # Retrieve metadata (this can take a moment)
    try:
        print("Fetching YouTube metadata...")
        meta: YouTubeMetadata = await extract_info(url)
        print("Fetched YouTube metadata...")
    except Exception as exc:  # pragma: no cover
        embed = discord.Embed(
            title="YouTube Error",
            description=f"Failed to fetch video information: {exc}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    # Attempt to start playback
    try:
        await play_url(ctx, meta.stream_url)
    except PlaybackError as exc:
        embed = discord.Embed(
            title="Playback Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    # Success – send now-playing embed
    minutes, seconds = divmod(meta.duration, 60)
    embed = discord.Embed(
        title=meta.title,
        url=meta.webpage_url,
        description=f"Duration: {minutes}:{seconds:02d}",
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=meta.thumbnail)
    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    """Register the !play command with the bot."""
    bot.add_command(commands.Command(play, name="play", help="Play YouTube audio"))