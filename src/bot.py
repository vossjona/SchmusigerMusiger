import ctypes

import discord
from discord.ext import commands

from command_handler import CommandHandler
from settings import Settings, BotConfig

# Load settings (reads .env then config.yml)
settings = Settings()
bot_config = BotConfig()

if not discord.opus.is_loaded():
    discord.opus.load_opus(settings.OPUS_LIB_NAME)
assert discord.opus.is_loaded(), "Opus failed to load!"

# Intents
intents = discord.Intents.default()
intents.message_content = True

# Bot setup
bot = commands.Bot(
    command_prefix=bot_config.prefix,
    intents=intents,
    description="Minimal music-bot MVP"
)

@bot.event
async def on_ready():
    print(f"[+] Logged in as {bot.user} (ID: {bot.user.id})")
    print("Registered commands:", [c.name for c in bot.commands])

# Load commands via handler
cmd_handler = CommandHandler(bot)
cmd_handler.load_commands()

if __name__ == "__main__":
    print(settings)
    print(bot_config)
    bot.run(settings.DISCORD_TOKEN.get_secret_value())