class PlaybackError(Exception):
    """Raised for any recoverable playback-related failure."""


class HumanError(Exception):
    """Raised when the user makes an invalid request."""
