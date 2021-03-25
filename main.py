import os
import discord
from discord.ext import commands
from discord import abc
import requests
import random
import datetime
import asyncio
from bs4 import BeautifulSoup as bs


intents = discord.Intents.default()
intents.members = True

settings = {
    'bot': 'Легенда Посмертия',
    'id': 769829547159322624,
    'prefix': '%'
}
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, case_insensitive=True)
TOKEN = os.getenv('TOKEN')

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

def timeNY():
    now = datetime.datetime.today()
    NY = datetime.datetime(2022, 1, 1)
    d = NY - now
    mm, ss = divmod(d.seconds, 60)
    hh, mm = divmod(mm, 60)
    return ('{} дней {} часа {} мин {} сек.'.format(d.days, hh-3, mm, ss))


@bot.event  #  Стримит...
async def on_ready():
    while True:
        steam = discord.Streaming(name="Your Tsukuyomi", url="https://www.twitch.tv/yourtsukuyomi")
        await bot.change_presence(status=discord.Status.online, activity=steam)

category_id = 797843720690860032  # id категории
make_channel_id = 797843749585551371  # id канала, для создания временных каналов
temp = []


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel:
        if after.channel.id == make_channel_id:
            guild = member.guild  # достём guild

            # достаём категорию, здесь нужно исправить, но я не помню что и как
            # по итогу здесь должен быть объект категории
            category = discord.utils.get(guild.categories, id=category_id)

            # создаём канал в категории
            created_channel = await guild.create_voice_channel(
                f'{member.display_name} channel',
                # position=3,
                category=category,
                bitrate=96000
            )

            # устанавливаем права
            await created_channel.set_permissions(member, connect=True, mute_members=True, move_members=True, manage_channels=True)
            # двигаем пользователя в канал
            await member.move_to(created_channel)
            # чтобы ничего не ждать, сохраняем id канала
            temp.append(created_channel.id)

    # алгоритм удаления
    if before.channel:
        # проверяем id в списке
        if before.channel.id in temp:
            # если нет пользователей - удаляем
            if not before.channel.members:
                return await before.channel.delete()


@bot.event
async def on_command_error(ctx, error):
    author = ctx.message.author
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=0x5B3375, description=f'{author.mention}, у тебя нет здесь власти!')
        await ctx.send(embed=embed)
        return

bot.run(TOKEN)  # Обращаемся к словарю settings с ключом token, для получения токена