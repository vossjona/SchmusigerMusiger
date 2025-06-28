import discord
from discord.ext import commands
from settings import Settings, BotConfig

# Load settings (reads .env then config.yml)
settings = Settings()
bot_config = BotConfig()

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

@bot.command(name="test")
async def test_cmd(ctx: commands.Context):
    """Responds with the configured greeting."""
    await ctx.send(bot_config.greeting)

if __name__ == "__main__":
    print(settings)
    print(bot_config)
    bot.run(settings.DISCORD_TOKEN.get_secret_value())
