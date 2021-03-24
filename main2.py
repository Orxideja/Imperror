import discord, asyncio, os, platform, sys
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
settings = {
    'bot': 'Легенда Посмертия',
    'id': 769829547159322624,
    'prefix': '%'
}
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, case_insensitive=True)
TOKEN = os.getenv('TOKEN')

# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
	bot.loop.create_task(status_task())
	print(f"Logged in as {bot.user.name}")
	print(f"Discord.py API version: {discord.__version__}")
	print(f"Python version: {platform.python_version()}")
	print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
	print("-------------------")

# Setup the stream status task of the bot
async def status_task():
	while True:
        stream = discord.Streaming(name="Your Tsukuyomi", url="https://www.twitch.tv/yourtsukuyomi")
        await bot.change_presence(discord.Status.online, activity=stream))

if __name__ == "__main__":
	for file in os.listdir("./cogs"):
		if file.endswith(".py"):
			extension = file[:-3]
			try:
				bot.load_extension(f"cogs.{extension}")
				print(f"Loaded extension '{extension}'")
			except Exception as e:
				exception = f"{type(e).__name__}: {e}"
				print(f"Failed to load extension {extension}\n{exception}")

# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
	# Ignores if a command is being executed by a bot or by the bot itself
	if message.author == bot.user or message.author.bot:
		return
	# Ignores if a command is being executed by a blacklisted user
	await bot.process_commands(message)

# Run the bot with the token
bot.run(TOKEN)