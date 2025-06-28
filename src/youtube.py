import asyncio
import logging

from pydantic import BaseModel
from yt_dlp import YoutubeDL
from audio_manager import PlaybackError

logger = logging.getLogger(__name__)


class YouTubeMetadata(BaseModel):
    """Subset of the metadata we care about for playback/showing embeds."""
    title: str
    duration: int          # seconds
    thumbnail: str
    webpage_url: str
    stream_url: str


async def extract_info(url: str) -> YouTubeMetadata:
    def _sync_extract(target_url: str) -> YouTubeMetadata:
        ydl_opts = {
            "skip_download":    True,
            "quiet":            False,           # for debugging
            "dump_single_json": True,
            "format":           "bestaudio/best",
            "socket_timeout":   10,
            "noplaylist":       True,
            "playlist_items":   "1",
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
            },
            "logger": logger,                     # attach your yt-dlp logger
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
        return YouTubeMetadata(
            title       = info["title"],
            duration    = int(info["duration"]),
            thumbnail   = info["thumbnail"],
            webpage_url = info["webpage_url"],
            stream_url  = info["url"],
        )

    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_sync_extract, url),
            timeout=30.0,
        )
    except asyncio.TimeoutError:
        raise PlaybackError("Timed out while fetching video info.")

