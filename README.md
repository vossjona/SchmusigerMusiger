# Discord Music Bot

A Discord music bot built with Python that streams audio from YouTube directly into voice channels. The bot supports queue management, search functionality, and various playback controls.

## Features

### 🎵 Core Playback
- **Stream YouTube audio** directly to Discord voice channels
- **Play by URL or search query** - supports both YouTube URLs and text searches
- **High-quality audio streaming** with FFmpeg and Opus encoding
- **Volume control** (0-100%) with real-time adjustment
- **Pause/Resume functionality** for active playback

### 📋 Queue Management
- **Smart queue system** - automatically plays next song when current ends
- **Add songs to queue** while music is playing
- **View current queue** with song details and durations
- **Skip to specific positions** in the queue
- **Remove individual songs** from any queue position
- **Shuffle queue** for randomized playback order
- **Clear entire queue** when needed

### 🔍 Search & Discovery
- **Interactive search results** - search YouTube and select from up to 10 results
- **Emoji-based selection** - react with number emojis to choose songs
- **Rich embeds** showing song titles, durations, and thumbnails

### 🎛️ Advanced Controls
- **Skip current track** or jump to specific queue positions
- **Now playing display** with song metadata and progress info
- **Queue status overview** showing current song and upcoming tracks
- **Automatic queue progression** - seamlessly transitions between songs

### 🛠️ User Experience
- **Intuitive commands** with aliases for quick access
- **Rich Discord embeds** for all responses and status updates
- **Error handling** with helpful, humorous error messages
- **Command validation** with clear usage instructions

## Installation

### Prerequisites
- Python 3.12 or higher
- FFmpeg installed and accessible in PATH
- Opus library for audio encoding
- Discord bot token from Discord Developer Portal

### System Dependencies

#### macOS (Homebrew)
```bash
brew install ffmpeg opus
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg libopus0 libopus-dev
```

#### Windows
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Add FFmpeg to your system PATH
3. Install Opus library or use the bundled version

### Python Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd music_bot
```

2. **Install dependencies**
```bash
pip install -e .
```

3. **Configure environment**
```bash
cp .env.example .env
```

4. **Edit `.env` file**
```env
DISCORD_TOKEN=your_discord_bot_token_here
OPUS_LIB_NAME=/path/to/your/opus/library
```

### Discord Bot Setup

1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token
5. Enable "Message Content Intent" in bot settings
6. Invite bot to your server with permissions:
   - Send Messages
   - Use Slash Commands
   - Connect to Voice
   - Speak in Voice
   - Use Voice Activity

### Configuration

Create `configs/config.yml`:
```yaml
prefix: "!"  # Command prefix (default: !)
```

## Usage

### Starting the Bot
```bash
cd src
python bot.py
```

### Basic Commands

#### Playback Controls
- `!play <url or search terms>` - Play audio from YouTube URL or search
- `!pause` - Pause current playback
- `!resume` - Resume paused playback
- `!stop` - Stop playback and clear queue
- `!volume [0-100]` - Set or check volume level

#### Queue Management
- `!queue` - Show current queue and now playing
- `!skip` - Skip to next song in queue
- `!skipto <number>` - Skip to specific position in queue
- `!remove <number>` - Remove song at specific position
- `!clear` - Clear entire queue
- `!shuffle` - Randomly shuffle queue order

#### Information & Search
- `!search <query>` - Search YouTube and select from results
- `!current` - Show currently playing song
- `!info` - Show bot information

### Command Examples

```bash
# Play a song by URL
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Search and play
!play never gonna give you up

# Advanced search with options
!search rick astley -- limit 3

# Queue management
!queue          # View current queue
!skip           # Skip current song
!skipto 3       # Jump to 3rd song in queue
!remove 2       # Remove 2nd song from queue
!shuffle        # Randomize queue order

# Volume control
!volume 75      # Set volume to 75%
!volume         # Check current volume
```

### Command Aliases

Most commands have shorter aliases for convenience:

| Command    | Aliases           |
|------------|-------------------|
| `!play`    | `!p`, `!start`    |
| `!search`  | `!s`, `!find`     |
| `!queue`   | `!q`, `!list`     |
| `!current` | `!np`, `!playing` |
| `!skip`    | `!next`, `!n`     |
| `!skipto`  | `!jump`           |
| `!remove`  | `!rm`, `!delete`  |
| `!shuffle` | `!sh`, `!random`  |
| `!volume`  | `!vol`, `!v`      |
| `!clear`   | `!empty`          |
| `!stop`    | `!stopp`, `!x`    |

## Architecture

### Project Structure
```
music_bot/
├── src/
│   ├── commands/           # Command modules
│   │   ├── control_commands.py    # Play, pause, stop, volume
│   │   ├── queue_commands.py      # Queue management
│   │   ├── search_commands.py     # Search functionality
│   │   └── info_commands.py       # Bot information
│   ├── audio_manager.py    # Audio playback management
│   ├── music_queue.py      # Queue data structure
│   ├── youtube.py          # YouTube integration
│   ├── command_handler.py  # Command loading system
│   ├── exceptions.py       # Custom exceptions
│   ├── settings.py         # Configuration management
│   ├── utils.py           # Utility functions
│   └── bot.py             # Main bot entry point
├── configs/
│   └── config.yml         # Bot configuration
├── .env                   # Environment variables
└── pyproject.toml         # Python dependencies
```

## Troubleshooting

### Common Issues

#### "Opus failed to load"
- **Cause**: Opus library not found or incorrect path
- **Solution**: Install Opus library and update `OPUS_LIB_NAME` in `.env`

#### "You are not connected to a voice channel"
- **Cause**: User not in voice channel when using play command
- **Solution**: Join a voice channel before using music commands

#### "Failed to fetch video information"
- **Cause**: YouTube URL invalid or video unavailable
- **Solution**: Check URL validity and video availability

#### "Timed out while searching"
- **Cause**: Network issues or YouTube rate limiting
- **Solution**: Wait a moment and try again with different search terms

#### Bot not responding to commands
- **Cause**: Missing message content intent or incorrect prefix
- **Solution**: Enable "Message Content Intent" in Discord Developer Portal

### Debug Mode

Enable detailed logging by modifying the bot startup:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tips

- **Queue Size**: Keep queue under 50 songs for optimal performance
- **Search Limits**: Use reasonable search limits (1-10 results)
- **Network**: Ensure stable internet connection for streaming
- **Resources**: Bot uses minimal CPU/RAM but requires good network bandwidth

## Development

### Adding New Commands

1. Create command function in appropriate module under `src/commands/`
2. Add command registration in module's `setup()` function
3. Commands are automatically loaded by `CommandHandler`

Example:
```python
async def my_command(ctx: commands.Context):
    """My custom command."""
    await ctx.send("Hello, world!")

def setup(bot: commands.Bot):
    bot.add_command(commands.Command(my_command, name="hello"))
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Support

For issues, feature requests, or questions:
1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information

