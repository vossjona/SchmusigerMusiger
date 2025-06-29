import random
from typing import List, Optional

from youtube import YouTubeMetadata


class MusicQueue:
    """Manages the music playback queue and current song state."""

    def __init__(self):
        self._queue: List[YouTubeMetadata] = []
        self._current: Optional[YouTubeMetadata] = None

    def add(self, metadata: YouTubeMetadata) -> None:
        """Add a song to the end of the queue."""
        self._queue.append(metadata)

    def remove(self, index: int) -> Optional[YouTubeMetadata]:
        """Remove and return the song at the given index (1-based)."""
        if 1 <= index <= len(self._queue):
            return self._queue.pop(index - 1)
        return None

    def clear(self) -> None:
        """Clear all songs from the queue."""
        self._queue.clear()

    def skip(self) -> Optional[YouTubeMetadata]:
        """Remove and return the next song in the queue."""
        if self._queue:
            return self._queue.pop(0)
        return None

    def skip_n(self, n: int) -> Optional[YouTubeMetadata]:
        """Skip to the nth song in the queue, removing all songs before it."""
        if n < 1 or n > len(self._queue):
            return None

        # Remove songs 1 through n-1
        for _ in range(n - 1):
            if self._queue:
                self._queue.pop(0)

        # Return the nth song (now at index 0)
        if self._queue:
            return self._queue.pop(0)
        return None

    def shuffle(self) -> None:
        """Randomly shuffle the order of songs in the queue."""
        random.shuffle(self._queue)

    def get_current(self) -> Optional[YouTubeMetadata]:
        """Get the currently playing song metadata."""
        return self._current

    def set_current(self, metadata: Optional[YouTubeMetadata]) -> None:
        """Set the currently playing song."""
        self._current = metadata

    def get_queue(self) -> List[YouTubeMetadata]:
        """Get a copy of the current queue."""
        return self._queue.copy()

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._queue) == 0

    def size(self) -> int:
        """Get the number of songs in the queue."""
        return len(self._queue)


# Global queue instance
music_queue = MusicQueue()