import discord
from discord.ext import commands

from exceptions import HumanError
from youtube import search_youtube
from commands.control_commands import play


async def search(ctx: commands.Context, query: str = None, source: str = "youtube", limit: int = 5):
    """Search for a song using the provided query."""
    try:
        if not query or not isinstance(query, str) or query.strip() == "":
            raise HumanError("Please provide a search query. Usage: `!search <query>`")
        
        # Validate source parameter
        if source not in ["youtube"]:
            raise HumanError(f"Unsupported source '{source}'. Currently only 'youtube' is supported.")
        
        # Validate limit parameter
        if not isinstance(limit, int):
            raise HumanError("Limit must be a whole number.")
        
        if limit < 1 or limit > 10:
            raise HumanError("Limit must be between 1 and 10.")
        
        # Send searching message
        search_embed = discord.Embed(
            title="Searching...",
            description=f"Searching for '{query}' on {source}...",
            color=discord.Color.yellow(),
        )
        search_message = await ctx.send(embed=search_embed)
        
        # Perform search
        try:
            results = await search_youtube(query, limit)
        except Exception as exc:
            embed = discord.Embed(
                title="Search Error",
                description=f"Failed to search for videos: {exc}",
                color=discord.Color.red(),
            )
            await search_message.edit(embed=embed)
            return
        
        if not results:
            embed = discord.Embed(
                title="No Results",
                description=f"No videos found for query: {query}",
                color=discord.Color.orange(),
            )
            await search_message.edit(embed=embed)
            return
        
        # Create embed with search results
        embed = discord.Embed(
            title=f"Search Results for '{query}'",
            description=f"Found {len(results)} result(s) from {source}",
            color=discord.Color.blue(),
        )
        
        # Add fields for each result
        for i, result in enumerate(results, 1):
            minutes, seconds = divmod(result.duration, 60)
            embed.add_field(
                name=f"{i}. {result.title}",
                value=f"Duration: {minutes}:{seconds:02d}\n[Watch on YouTube]({result.webpage_url})",
                inline=False
            )
        
        embed.set_footer(text="React with number emojis (1️⃣-🔟) to play a song!")
        
        # Update the search message with results
        await search_message.edit(embed=embed)
        message = search_message
        
        # Add number reactions
        number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for i in range(len(results)):
            await message.add_reaction(number_emojis[i])
        
        # Wait for user reaction
        def check(reaction, user):
            return (
                user == ctx.author and 
                str(reaction.emoji) in number_emojis[:len(results)] and 
                reaction.message.id == message.id
            )
        
        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=60.0, check=check)
            
            # Get the selected result index
            selected_index = number_emojis.index(str(reaction.emoji))
            selected_result = results[selected_index]
            
            # Clear reactions after selection
            try:
                await message.clear_reactions()
            except:
                pass  # Ignore permission errors
            
            # Actually invoke the play command
            await play(ctx, selected_result.webpage_url)
            
        except TimeoutError:
            # Remove reactions after timeout
            try:
                await message.clear_reactions()
            except:
                pass  # Ignore permission errors
            
    except HumanError as exc:
        embed = discord.Embed(
            title="Human Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


async def song_info(ctx: commands.Context, url: str = None):
    """Show information about a specific song."""
    try:
        if not url or not isinstance(url, str) or url.strip() == "":
            raise HumanError("Please provide a song URL. Usage: `!song_info <url>`")
        
        # Todo
        embed = discord.Embed(
            title="Work in Progress",
        )
        await ctx.send(embed=embed)
    except HumanError as exc:
        embed = discord.Embed(
            title="Human Error",
            description=str(exc),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_command(commands.Command(search, name="search", help="Search for a song"))
    bot.add_command(commands.Command(song_info, name="song_info", help="Show information about a specific song"))


