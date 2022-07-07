import os
import discord
from discord.ext import commands
import youtube_dl
from discord import abc
import requests
import random
import datetime
import asyncio
from bs4 import BeautifulSoup as bs
from asyncio import sleep


intents = discord.Intents.default()
intents.members = True

settings = {
    'bot': 'Малюсенькая Чича',
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


headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 YaBrowser/19.9.0.1343 Yowser/2.5 Safari/537.36'}

base_url = 'https://pikabu.ru/community/steam'


@bot.command(pass_context=True)
async def free(ctx):
    await ctx.message.delete()
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    soup = bs(request.content, 'lxml')
    title = soup.find('h2', attrs={'story__title'}).text
    href = soup.find('a', attrs={'story__title-link'})['href']
    img = soup.find('img', attrs={'story-image__image'})['data-src']
    content_text = soup.find('div', attrs={'story-block story-block_type_text'}).text
    embed = discord.Embed(color=0x5B3375, description=title + "\n" + content_text + "\n" + href)
    embed.set_image(url=img)
    await ctx.send(embed=embed)


@bot.event  #  Стримит...
async def on_ready():
    while True:
        steam = discord.Streaming(name="Your Tsukuyomi", url="https://www.twitch.tv/yourtsukuyomi")
        await bot.change_presence(status=discord.Status.online, activity=steam)

category_id = 994453005707526196  # id категории
make_channel_id = 994464863592132689  # id канала, для создания временных каналов
temp = []


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel:
        if after.channel.id == make_channel_id:
            guild = member.guild  # достём guild


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


@bot.command(pass_context=True)
async def reactionGetter(ctx, msg):
    cache_msg = discord.utils.get(bot.cached_messages, id=msg.id) #or client.messages depending on your variable
    await ctx.send(cache_msg.reactions)


@bot.event
async def on_command_error(ctx, error):
    author = ctx.message.author
    # if command has local error handler, return
    # if hasattr(ctx.command, 'on_error'):
    #     return
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=0x5B3375, description=f'{author.mention}, у тебя нет здесь власти!')
        await ctx.send(embed=embed)
        return


@bot.event
async def on_message(message):
    channels = (797841049707479142, 805759773944315905, 805759934167515196, 994460630956376164, 994460954848931901, 994461134717452288, 994461220105093181)
    if message.channel in channels:
        for x in (967697970973802507, 967697970973802507, 967697470324895774, 967697475915878420, 967697487483797555, 967697505255055402):
            return await bot.add_reaction(message, x)

bot.run(TOKEN)  # Обращаемся к словарю settings с ключом token, для получения токена