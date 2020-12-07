import os
import discord
from discord.ext import commands
from discord import abc
import requests
import random
import datetime

settings = {
    'bot': 'Гейша Императора',
    'id': 769829547159322624,
    'prefix': '%'
}
bot = commands.Bot(command_prefix=settings['prefix']) # Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.
TOKEN = os.getenv('TOKEN')


def timeNY():
    now = datetime.datetime.today()
    NY = datetime.datetime(2021, 1, 1)
    d = NY - now  # str(d)  '83 days, 2:43:10.517807'
    mm, ss = divmod(d.seconds, 60)
    hh, mm = divmod(mm, 60)
    return ('{} дней {} часа {} мин {} сек.'.format(d.days, hh, mm, ss))

@bot.event  #  Играет в...
async def on_ready():
    while True:
        game = discord.Game("PADORU PADORU")
        await bot.change_presence(status=discord.Status.idle, activity=game)


# @bot.event
# async def on_command_error(ctx, error):
#     author = ctx.message.author
#     # if command has local error handler, return
#     if hasattr(ctx.command, 'on_error'):
#         return
#     if isinstance(error, commands.MissingPermissions):
#         embed = discord.Embed(color=0x5B3375, description=f'{author.mention}, у тебя нет здесь власти!')
#         await ctx.send(embed=embed)
#         return


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
    gifs = ['https://cdn.discordapp.com/attachments/770262193949507656/785177869139443722/tenor_1.gif',
          'https://media.discordapp.net/attachments/738296780009111583/783760232253489172/1575476244_388.gif',
          'https://cdn.discordapp.com/attachments/770262193949507656/785177871386673192/tenor_2.gif',
          'https://cdn.discordapp.com/attachments/770262193949507656/785177861413142548/tenor_3.gif',
          'https://cdn.discordapp.com/attachments/770262193949507656/785177875452133416/tenor_4.gif',
          'https://cdn.discordapp.com/attachments/770262193949507656/785177872507600906/tenor_5.gif']
    days = timeNY()
    text = [f'С наступающим новым годом, {author.mention}!',
            f'Уютного декабря и праздничного настроения, {author.mention}!',
            f'Побольше снега и гирлянд тебе, {author.mention}']
    embed = discord.Embed(color=0x5B3375, description=random.choice(text) + f'\n {days} until Padoru')
    embed.set_image(url=random.choice(gifs))
    await ctx.send(embed=embed)


# @bot.command(aliases=["8ball"])
# async def шар(ctx, *, question):
#     responses = ["might be",
#                  "yes",
#                  "i point to yes",
#                  "i think so",
#                  "maybe ¯\_(ツ)_/¯ ",
#                  "very lazy ask later",
#                  "zzzzzzzzzzzzz",
#                  "wait what?",
#                  "no",
#                  "WHO AM I TO YOU?!",
#                  "CREEPER!",
#                  "idk",
#                  "¯\_(ツ)_/¯",
#                  "doge  'aka:yes'",
#                  "i dont think so",
#                  "idgi",
#                  "nope",
#                  "doubtfull",
#                  "more likely",
#                  "play minecraft"
#                  ]
#     await ctx.send(f"{question}+\n + {random.choice(responses)}")

@bot.command(help='Команда поиска картинки по слову')
async def pic(ctx, keyword):
    author = ctx.message.author
    await ctx.send(f'{author.mention}, ищу картиночку, ожидайте...', delete_after=3)
    response = requests.get('https://source.unsplash.com/1600x900/?'+keyword)  # Get-запрос
    embed = discord.Embed(color=0x5B3375)  # Создание Embed'a
    embed.set_image(url=response.url)  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


@bot.command(help='Команда поиска рандомной картинки')
async def randompic(ctx):
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
async def chnick(ctx, member: discord.Member, *, nick):
    try:
        await member.edit(nick=nick)
        embed = discord.Embed(color=0x5B3375, description=f'Никнейм был изменён на {member.mention} ')
        await ctx.send(embed=embed)
    except discord.ext.commands.errors.MissingPermissions(administrator=True):
        embed = discord.Embed(color=0x5B3375, description='У тебя нет здесь власти!')
        await ctx.send(embed=embed)


@bot.command(help='create-channel')
async def create_channel(ctx):
    guild = ctx.guild
    author = ctx.message.author
    channel_name = author+'s торги'
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        embed = discord.Embed(color=0x5B3375, description=f'Creating a new channel: {channel_name}')
        await ctx.send(embed=embed)
        await guild.create_voice_channel(channel_name)

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