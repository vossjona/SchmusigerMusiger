import logging
from typing import Callable, Optional

import discord
from discord.ext import commands

from exceptions import PlaybackError, HumanError
from music_queue import music_queue

logger = logging.getLogger(__name__)

# Global volume state (0.0 to 1.0)
_current_volume: float = 0.5


async def play_url(ctx: commands.Context, url: str, on_complete: Optional[Callable] = None) -> None:
    """
    Join the command author's voice channel (if not already connected) and
    stream the provided audio URL via FFmpeg.

    Parameters
    ----------
    ctx : commands.Context
        The Discord command context
    url : str
        The audio URL to stream
    on_complete : Optional[Callable]
        Callback function to execute when playback completes

    Raises
    ------
    PlaybackError
        If the user is not connected to voice, the bot is already connected to
        another channel, or FFmpeg fails to start.
    """
    voice_state = ctx.author.voice
    if voice_state is None:
        raise PlaybackError("You are not connected to a voice channel.")

    channel = voice_state.channel
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]

    if voice_client and voice_client.channel != channel:
        raise PlaybackError("I am already connected to another voice channel.")

    if not voice_client:
        voice_client = await channel.connect()

    # Stop any previous audio
    if voice_client.is_playing() or voice_client.is_paused():
        voice_client.stop()

    ffmpeg_opts = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    source = discord.FFmpegPCMAudio(
        url,
        executable="ffmpeg",
        **ffmpeg_opts,
    )
    
    # Apply volume control
    source = discord.PCMVolumeTransformer(source, volume=_current_volume)

    def _after(err: Exception | None) -> None:
        if err:
            logger.error("Player error: %s", err)
        else:
            # Song completed successfully, trigger callback if provided
            if on_complete:
                try:
                    # Use asyncio to run the callback in the event loop
                    import asyncio
                    asyncio.create_task(on_complete())
                except Exception as callback_err:
                    logger.error("Callback error: %s", callback_err)

    try:
        voice_client.play(source, after=_after)
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to start playback")
        raise PlaybackError("Failed to start playback.") from exc


async def play_next_in_queue(ctx: commands.Context) -> bool:
    """
    Play the next song in the queue automatically.
    
    Returns
    -------
    bool
        True if a song was played, False if queue is empty
    """
    next_song = music_queue.skip()
    if next_song:
        music_queue.set_current(next_song)
        try:
            # Create a callback that will play the next song when this one ends
            async def queue_callback():
                await play_next_in_queue(ctx)
            
            await play_url(ctx, next_song.stream_url, on_complete=queue_callback)
            return True
        except PlaybackError as exc:
            logger.error("Failed to play next song in queue: %s", exc)
            # Try to continue with the next song
            await play_next_in_queue(ctx)
            return False
    else:
        # Queue is empty, clear current song
        music_queue.set_current(None)
        return False


async def stop_playback(ctx: commands.Context) -> None:
    """
    Stop playback and clear the queue.
    
    Raises
    ------
    HumanError
        If no audio is currently playing.
    """
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]
    
    if not voice_client or (not voice_client.is_playing() and not voice_client.is_paused()):
        raise HumanError("No audio is currently playing.")
    
    voice_client.stop()
    music_queue.clear()
    music_queue.set_current(None)


async def pause_playback(ctx: commands.Context) -> None:
    """
    Pause the currently playing audio.

    Raises
    ------
    HumanError
        If no audio is currently playing.
    """
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]
    
    if not voice_client or not voice_client.is_playing():
        raise HumanError("No audio is currently playing.")
    
    voice_client.pause()


async def resume_playback(ctx: commands.Context) -> None:
    """
    Resume paused audio playback.

    Raises
    ------
    HumanError
        If no audio is currently paused.
    """
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]
    
    if not voice_client or not voice_client.is_paused():
        raise HumanError("No audio is currently paused.")
    
    voice_client.resume()


async def set_volume(ctx: commands.Context, volume: int) -> None:
    """
    Set the playback volume for future audio.
    
    Parameters
    ----------
    ctx : commands.Context
        The Discord command context
    volume : int
        Volume level from 0 to 100
        
    Raises
    ------
    HumanError
        If volume is not between 0 and 100
    """
    global _current_volume
    
    if not (0 <= volume <= 100):
        raise HumanError("Volume level must be between 0 and 100.")
    
    _current_volume = volume / 100.0
    
    # If audio is currently playing, update its volume
    voice_client: discord.VoiceClient | None = ctx.guild.voice_client  # type: ignore[attr-defined]
    if voice_client and hasattr(voice_client.source, 'volume'):
        voice_client.source.volume = _current_volume


def get_volume() -> int:
    """
    Get the current volume level as a percentage (0-100).
    
    Returns
    -------
    int
        Current volume level
    """
    return int(_current_volume * 100)
