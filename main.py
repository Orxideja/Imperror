import os
import discord
from discord.ext import commands
from discord import abc
import requests
from discord.utils import get
import akinator
from akinator.async_aki import Akinator
import time
import asyncio

settings = {
    'bot': 'Гейша Императора',
    'id': 769829547159322624,
    'prefix': '%'
}
bot = commands.Bot(command_prefix=settings['prefix']) # Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
TOKEN = os.getenv('TOKEN')


@bot.event  #  Играет в...
async def on_ready():
    while True:
        game = discord.Game("PADORU PADORU")
        await bot.change_presence(status=discord.Status.idle, activity=game)


# @bot.event
# async def on_message(message):
#     if ':EmojiName:' in message.content:
#         emoji = get(bot.get_all_emojis(), name='EmojiName')
#         await bot.add_reaction(message, emoji)
#         await bot.process_commands(message)


@bot.command(help='Команда приветствия') # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx):  # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.

    await ctx.send(f'Кукусики, {author.mention}!')  # Выводим сообщение с упоминанием автора, обращаясь к переменной author.


@bot.command(help='Команда поздравления') # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def padoru(ctx):  # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
    image = requests.get('https://media.discordapp.net/attachments/738296780009111583/783760232253489172/1575476244_388.gif')
    embed = discord.Embed(color=0x5B3375, description=f"С наступающим новым годом, {author.mention}!", image=image)
    await ctx.send(embed=embed)


@bot.command(help='Команда поиска картинки по слову')
async def pic(ctx, keyword):
    author = ctx.message.author
    await ctx.send(f'{author.mention}, ищу картиночку, ожидайте...', delete_after=3)
    response = requests.get('https://source.unsplash.com/1600x900/?'+keyword)  # Get-запрос
    embed = discord.Embed(color=0x5B3375)  # Создание Embed'a
    embed.set_image(url=response.url)  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


@bot.command(help='Команда поиска рандомной картинки')
async def random(ctx):
    author = ctx.message.author
    await ctx.send(f'{author.mention}, ищу картиночку, ожидайте...', delete_after=3)
    response = requests.get('https://source.unsplash.com/1600x900/')  # Get-запрос
    embed = discord.Embed(color=0x5B3375)  # Создание Embed'a
    embed.set_image(url=response.url)  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


@bot.command(help='адм.команда-добавление роли юзеру')
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    embed = discord.Embed(color=0x5B3375, description=f"Юзеру {user.mention} была выдана роль: {role.mention}")
    await ctx.send(embed=embed)


@bot.command(help='адм.команда-удаление роли юзера')
@commands.has_permissions(administrator=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    embed = discord.Embed(color=0x5B3375, description=f"С юзера {user.mention} была снята роль: {role.mention}")
    await ctx.send(embed=embed)


@bot.command(help='адм.команда-удаление сообщений')
@commands.has_permissions(administrator=True)
async def clear(ctx, num):
    msg = []  # Empty list to put all the messages in the log
    num = int(num)  # Converting the amount of messages to delete to an integer
    async for x in abc.Messageable.history(ctx.message.channel, limit=num):
        msg.append(x)
    await ctx.channel.delete_messages(msg)
    embed = discord.Embed(color=0x5B3375, description=f"{num} сообщений было удалено")
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def chnick(ctx, member: discord.Member, nick1='', nick2='', nick3='', nick4='', nick5='', nick6=''):
    try:
        nick = str(nick1 + ' ' + nick2 + ' ' + nick3 + ' ' + nick4 + ' ' + nick5 + ' ' + nick6)
        await member.edit(nick=nick)
        embed = discord.Embed(color=0x5B3375, description=f'Никнейм был изменён на {member.mention} ')
        await ctx.send(embed=embed)
    except discord.ext.commands.errors.MissingPermissions(administrator=True):
        embed = discord.Embed(color=0x5B3375, description='У тебя нет здесь власти!')
        await ctx.send(embed=embed)


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


@bot.command(help='create-channel')
async def create_channel(ctx):
    guild = ctx.guild
    author = ctx.message.author
    channel_name = author+'s торги'
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        embed = discord.Embed(color=0x5B3375, description=f'Creating a new channel: {channel_name}')
        await ctx.send(embed=embed)
        await guild.create_text_channel(channel_name)

# Voice mute and unmute
@bot.command()
@commands.has_permissions(administrator=True)
async def mutev(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Voice')
    await member.add_roles(mute_role)
    await member.edit(mute=True, deafen=True)
    await ctx.send(f'{member.mention} получил мут за плохое поведение!')


@bot.command()
@commands.has_permissions(administrator=True)
async def unmutev(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Voice')
    await member.remove_roles(mute_role)
    await member.edit(mute=False, deafen=False)
    await ctx.send(f'{member.mention} размьючен!')


@bot.command()
@commands.has_permissions(administrator=True)
async def mutec(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Chat')
    await member.add_roles(mute_role)
    await member.edit(deafen=True)
    await ctx.send(f'{member.mention} получил мут за плохое поведение!')


@bot.command()
@commands.has_permissions(administrator=True)
async def unmutec(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Chat')
    await member.remove_roles(mute_role)
    await member.edit(deafen=False)
    await ctx.send(f'{member.mention} размьючен!')
 # post = api.newsfeed.get(filters='post',counts=1,source_ids=group_id)


#  Часть с музыкой
@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = ctx.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send('успешно подключился')


@bot.command()
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = ctx.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.disconnect()
        await ctx.send('успешно отключился')

bot.run(TOKEN)  # Обращаемся к словарю settings с ключом token, для получения токена