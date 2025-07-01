import discord
from discord.ext import commands

from music_queue import music_queue
from audio_manager import play_next_in_queue
from exceptions import HumanError, get_random_human_error_title


async def queue(ctx: commands.Context):
    """Show the current playback queue."""
    current_song = music_queue.get_current()
    queue_list = music_queue.get_queue()
    
    if not current_song and music_queue.is_empty():
        embed = discord.Embed(
            title="Queue Empty",
            description="No songs in queue. Use `!play <url>` to add songs!",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="Music Queue",
        color=discord.Color.blue(),
    )
    
    # Show currently playing song
    if current_song:
        minutes, seconds = divmod(current_song.duration, 60)
        embed.add_field(
            name="🎵 Now Playing",
            value=f"**{current_song.title}**\nDuration: {minutes}:{seconds:02d}",
            inline=False
        )
    
    # Show queue
    if queue_list:
        queue_text = ""
        for i, song in enumerate(queue_list[:10], 1):  # Show first 10 songs
            minutes, seconds = divmod(song.duration, 60)
            queue_text += f"{i}. **{song.title}** ({minutes}:{seconds:02d})\n"
        
        if len(queue_list) > 10:
            queue_text += f"... and {len(queue_list) - 10} more songs"
        
        embed.add_field(
            name=f"📋 Up Next ({len(queue_list)} songs)",
            value=queue_text,
            inline=False
        )
    else:
        embed.add_field(
            name="📋 Up Next",
            value="Queue is empty",
            inline=False
        )
    
    await ctx.send(embed=embed)


async def now_playing(ctx: commands.Context):
    """Show the currently playing track."""
    current_song = music_queue.get_current()
    
    if not current_song:
        embed = discord.Embed(
            title="Nothing Playing",
            description="No song is currently playing. Use `!play <url>` to start playback!",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)
        return
    
    minutes, seconds = divmod(current_song.duration, 60)
    embed = discord.Embed(
        title="Now Playing",
        description=f"**{current_song.title}**\nDuration: {minutes}:{seconds:02d}",
        color=discord.Color.green(),
    )
    embed.set_thumbnail(url=current_song.thumbnail)
    embed.add_field(name="URL", value=f"[Watch on YouTube]({current_song.webpage_url})", inline=False)
    
    # Show queue size
    queue_size = music_queue.size()
    if queue_size > 0:
        embed.add_field(name="Queue", value=f"{queue_size} songs waiting", inline=True)
    
    await ctx.send(embed=embed)


async def clear_queue(ctx: commands.Context):
    """Clear the current playback queue."""
    if music_queue.is_empty():
        embed = discord.Embed(
            title="Queue Already Empty",
            description="The queue is already empty.",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)
        return
    
    queue_size = music_queue.size()
    music_queue.clear()
    
    embed = discord.Embed(
        title="Queue Cleared",
        description=f"Removed {queue_size} songs from the queue.",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


async def skip(ctx: commands.Context):
    """Skip the current track."""
    current_song = music_queue.get_current()
    
    if not current_song:
        embed = discord.Embed(
            title="Nothing to Skip",
            description="No song is currently playing.",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)
        return
    
    # Stop current playback
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]
    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
    
    # Try to play next song
    if await play_next_in_queue(ctx):
        next_song = music_queue.get_current()
        embed = discord.Embed(
            title="Skipped",
            description=f"Skipped **{current_song.title}**\nNow playing: **{next_song.title}**" if next_song else "Skipped song",
            color=discord.Color.green(),
        )
    else:
        embed = discord.Embed(
            title="Skipped",
            description=f"Skipped **{current_song.title}**\nQueue is now empty.",
            color=discord.Color.green(),
        )
    
    await ctx.send(embed=embed)


async def skip_n(ctx: commands.Context, n: int = None):
    """Skip the next N tracks in the queue."""
    try:
        if n is None:
            raise HumanError("Please provide a number. Usage: `!skip_n <number>`")
        
        if not isinstance(n, int):
            raise HumanError("Please provide a whole number. Usage: `!skip_n <number>`")
        
        if n < 1:
            raise HumanError("Please provide a number greater than 0.")
    except HumanError as exc:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    
    if n > music_queue.size():
        embed = discord.Embed(
            title="Invalid Skip",
            description=f"Cannot skip to position {n}. Queue only has {music_queue.size()} songs.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    
    current_song = music_queue.get_current()
    
    # Stop current playback
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]
    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
    
    # Skip to the nth song
    target_song = music_queue.skip_n(n)
    
    if target_song:
        music_queue.set_current(target_song)
        
        # Create callback for automatic queue progression
        async def queue_callback():
            await play_next_in_queue(ctx)
        
        try:
            from audio_manager import play_url
            await play_url(ctx, target_song.stream_url, on_complete=queue_callback)
            
            embed = discord.Embed(
                title=f"Skipped to Position {n}",
                description=f"Now playing: **{target_song.title}**",
                color=discord.Color.green(),
            )
        except Exception as exc:
            embed = discord.Embed(
                title="Playback Error",
                description=f"Failed to play skipped song: {exc}",
                color=discord.Color.red(),
            )
    else:
        music_queue.set_current(None)
        embed = discord.Embed(
            title="Queue Empty",
            description="Skipped songs but queue is now empty.",
            color=discord.Color.orange(),
        )
    
    await ctx.send(embed=embed)


async def remove_n(ctx: commands.Context, n: int = None):
    """Remove the Nth track from the queue."""
    try:
        if n is None:
            raise HumanError("Please provide a number. Usage: `!remove_n <number>`")
        
        if not isinstance(n, int):
            raise HumanError("Please provide a whole number. Usage: `!remove_n <number>`")
        
        if n < 1:
            raise HumanError("Please provide a number greater than 0.")
    except HumanError as exc:
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    
    removed_song = music_queue.remove(n)
    
    if removed_song:
        embed = discord.Embed(
            title="Song Removed",
            description=f"Removed **{removed_song.title}** from position {n}.",
            color=discord.Color.green(),
        )
    else:
        embed = discord.Embed(
            title="Invalid Position",
            description=f"No song at position {n}. Queue has {music_queue.size()} songs.",
            color=discord.Color.red(),
        )
    
    await ctx.send(embed=embed)


async def shuffle(ctx: commands.Context):
    """Shuffle the current playback queue."""
    if music_queue.is_empty():
        embed = discord.Embed(
            title="Queue Empty",
            description="Cannot shuffle an empty queue.",
            color=discord.Color.orange(),
        )
        await ctx.send(embed=embed)
        return
    
    music_queue.shuffle()
    
    embed = discord.Embed(
        title="Queue Shuffled",
        description=f"Randomly shuffled {music_queue.size()} songs in the queue.",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    """Register the queue commands with the bot."""
    bot.add_command(commands.Command(queue, name="queue", aliases=["q", "list"], help="Show the current playback queue"))
    bot.add_command(commands.Command(now_playing, name="current", aliases=["np", "playing"], help="Show the currently playing track"))
    bot.add_command(commands.Command(clear_queue, name="clear", aliases=["empty"], help="Clear the current playback queue"))
    bot.add_command(commands.Command(skip, name="skip", aliases=["next", "n"], help="Skip the current track"))
    bot.add_command(commands.Command(skip_n, name="skipto", aliases=["jump"], help="Skip the next N tracks in the queue"))
    bot.add_command(commands.Command(remove_n, name="remove", aliases=["rm", "delete"], help="Remove the Nth track from the queue"))
    bot.add_command(commands.Command(shuffle, name="shuffle", aliases=["sh", "random"], help="Shuffle the current playback queue"))
