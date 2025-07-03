import discord
from discord.ext import commands

from audio_manager import play_url, pause_playback, resume_playback, stop_playback, play_next_in_queue, set_volume, get_volume
from youtube import YouTubeMetadata, extract_info, search_youtube
from music_queue import music_queue
from utils import parse_query_and_args

from exceptions import HumanError, PlaybackError, get_random_human_error_title



async def play(ctx: commands.Context, *args):
    """Stream audio from a YouTube URL or search query into the caller's voice channel."""
    try:
        if not args:
            raise HumanError("Please provide a YouTube URL or search query. Usage: `!play <url or search terms>`")

        # Ensure the author is in a voice channel
        if ctx.author.voice is None:
            embed = discord.Embed(
                title="Voice Channel Required",
                description="You must be connected to a voice channel to use this command.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return
    except HumanError as exc:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    # Parse query and additional arguments
    query, additional_args = parse_query_and_args(args)

    if not query:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description="Please provide a YouTube URL or search query. Usage: `!play <url or search terms>`",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    # Check if it's a URL (contains youtube.com, youtu.be, etc.)
    is_url = any(domain in query.lower() for domain in ["youtube.com", "youtu.be", "music.youtube.com"])

    # Retrieve metadata (this can take a moment)
    try:
        if is_url:
            meta: YouTubeMetadata = await extract_info(query)
        else:
            # Search for the best match
            searching_embed = discord.Embed(
                title="Searching",
                description=f"Searching for: {query}",
                color=discord.Color.yellow(),
            )
            search_message = await ctx.send(embed=searching_embed)

            search_results = await search_youtube(query, limit=1)
            await search_message.delete()

            if not search_results:
                embed = discord.Embed(
                    title="No Results",
                    description=f"No search results found for: {query}",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
                return

            # Get full metadata including stream_url for the best match
            best_match = search_results[0]
            meta: YouTubeMetadata = await extract_info(best_match.webpage_url)

    except Exception as exc:  # pragma: no cover
        embed = discord.Embed(
            title="YouTube Error",
            description=f"Failed to fetch video information: {exc}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    # Check if something is currently playing
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]
    is_playing = voice_client and (voice_client.is_playing() or voice_client.is_paused())

    if is_playing:
        # Add to queue
        music_queue.add(meta)
        
        # Send queued embed
        minutes, seconds = divmod(meta.duration, 60)
        embed = discord.Embed(
            title="Added to Queue",
            description=f"**{meta.title}**\nDuration: {minutes}:{seconds:02d}\nPosition: {music_queue.size()}",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=meta.thumbnail)
        await ctx.send(embed=embed)
    else:
        # Play immediately
        music_queue.set_current(meta)
        
        # Create callback for automatic queue progression
        async def queue_callback():
            await play_next_in_queue(ctx)
        
        try:
            await play_url(ctx, meta.stream_url, on_complete=queue_callback)
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
            title="Now Playing",
            description=f"**{meta.title}**\nDuration: {minutes}:{seconds:02d}",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=meta.thumbnail)
        embed.add_field(name="URL", value=f"[Watch on YouTube]({meta.webpage_url})", inline=False)
        await ctx.send(embed=embed)


async def stop(ctx: commands.Context):
    """Stop playback and clear the queue."""
    try:
        await stop_playback(ctx)
        embed = discord.Embed(
            title="Stopped",
            description="Playback stopped and queue cleared.",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def pause(ctx: commands.Context):
    """Pause playback."""
    try:
        await pause_playback(ctx)
        embed = discord.Embed(
            title="Paused",
            description="Playback has been paused.",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def resume(ctx: commands.Context):
    """Resume playback."""
    try:
        await resume_playback(ctx)
        embed = discord.Embed(
            title="Resumed",
            description="Playback has been resumed.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def volume(ctx: commands.Context, level: int = None):
    """Set the playback volume (0-100)."""
    try:
        if level is None:
            # Show current volume
            current_vol = get_volume()
            embed = discord.Embed(
                title="Current Volume",
                description=f"Volume is set to {current_vol}%",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)
            return

        if not isinstance(level, int):
            raise HumanError("Please provide a volume level as a whole number (0-100).")

        await set_volume(ctx, level)
        
        embed = discord.Embed(
            title="Volume Set",
            description=f"Volume set to {level}%",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    """Register the !play command with the bot."""
    bot.add_command(commands.Command(play, name="play", aliases=["p", "start"], help="Play YouTube audio"))
    bot.add_command(commands.Command(stop, name="stop", aliases=["stopp", "x"], help="Stop playback and clear the queue"))
    bot.add_command(commands.Command(pause, name="pause", help="Pause playback"))
    bot.add_command(commands.Command(resume, name="resume", aliases=["unpause"], help="Resume playback"))
    bot.add_command(commands.Command(volume, name="volume", aliases=["vol", "v"], help="Set playback volume (0-100)"))
