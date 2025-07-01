import ctypes

import discord
from discord.ext import commands

from command_handler import CommandHandler
from settings import Settings, BotConfig
from exceptions import get_random_human_error_title

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

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Handle command errors."""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title=get_random_human_error_title(),
            description=f"Command `{ctx.invoked_with}` not found. Use `{bot_config.prefix}help` to see available commands.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
    else:
        # Re-raise other errors so they get logged
        raise error

# Load commands via handler
cmd_handler = CommandHandler(bot)
cmd_handler.load_commands()

if __name__ == "__main__":
    bot.run(settings.DISCORD_TOKEN.get_secret_value())
