import logging

import discord
from discord.ext import commands

from exceptions import PlaybackError, HumanError

logger = logging.getLogger(__name__)


async def play_url(ctx: commands.Context, url: str) -> None:
    """
    Join the command author's voice channel (if not already connected) and
    stream the provided audio URL via FFmpeg.

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

    def _after(err: Exception | None) -> None:
        if err:
            logger.error("Player error: %s", err)

    try:
        voice_client.play(source, after=_after)
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to start playback")
        raise PlaybackError("Failed to start playback.") from exc


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
