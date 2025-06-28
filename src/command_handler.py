import importlib
import pkgutil
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)

class CommandHandler:
    """
    Loads and registers command modules from the `commands` package.
    Each module must define a `setup(bot: commands.Bot)` function.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def load_commands(self) -> None:
        """Discover and load all command modules."""
        import commands as commands_pkg
        for finder, name, _ in pkgutil.iter_modules(commands_pkg.__path__):
            module_path = f"commands.{name}"
            print(f"Loading {module_path}")
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, "setup"):
                    module.setup(self.bot)
                    logger.info(f"Loaded command module: {name}")
                else:
                    logger.warning(f"Module {name} has no setup(bot) function.")
            except Exception as e:
                logger.error(f"Failed to load command {name}: {e}")