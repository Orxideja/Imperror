import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, case_insensitive=True)

initial_extensions = [
    "cogs.fun",
    "cogs.general"
]

if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension '{extension}'")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            print(f"Failed to load extension {extension}\n{exception}")

bot.run(TOKEN)
