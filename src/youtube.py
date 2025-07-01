import asyncio
import logging
from typing import List

from pydantic import BaseModel
from yt_dlp import YoutubeDL
from exceptions import PlaybackError

logger = logging.getLogger(__name__)


class YouTubeMetadata(BaseModel):
    """Subset of the metadata we care about for playback/showing embeds."""
    title: str
    duration: int          # seconds
    thumbnail: str
    webpage_url: str
    stream_url: str | None = None


async def search_youtube(query: str, limit: int = 5) -> List[YouTubeMetadata]:
    """Search YouTube for videos matching the query."""
    def _sync_search(search_query: str, max_results: int) -> List[YouTubeMetadata]:
        ydl_opts = {
            "skip_download": True,
            "quiet": False,
            "socket_timeout": 10,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"]
                }
            },
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
            },
            "logger": logger,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            # Search for videos
            search_results = ydl.extract_info(
                f"ytsearch{max_results}:{search_query}",
                download=False
            )
            
            results = []
            for entry in search_results.get("entries", []):
                if entry:
                    results.append(YouTubeMetadata(
                        title=entry["title"],
                        duration=int(entry["duration"]),
                        thumbnail=entry["thumbnail"],
                        webpage_url=entry["webpage_url"],
                        # stream_url is not available in search results
                    ))
            return results
    
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_sync_search, query, limit),
            timeout=30.0,
        )
    except asyncio.TimeoutError:
        raise PlaybackError("Timed out while searching for videos.")


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
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"]
                }
            },
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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

