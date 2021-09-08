import discord
import random
from discord.ext import commands
from discord import abc


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        """
        Get some useful (or not) information about the server.
        """
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"{server.owner}\n{server.owner.id}"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    @commands.command(name="hello")
    async def hello(self, context):  # Создаём функцию и передаём аргумент ctx.
        author = context.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
        await context.send(f'Кукусики, {author.mention}!')  # Выводим сообщение с упоминанием автора, обращаясь к переменной author.

    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        Create a poll where members can vote.
        """
        embed = discord.Embed(
            title=args
        )
        embed.set_footer(
            text=f"Голосование создано: {context.message.author} • Жмякайте реакцию!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="шар")
    async def шар(self, context, **args):
        responses = ["А ты как считаешь?",
                 "Определённо да",
                 "Конечно же нет",
                 'Боги говорят - "да"',
                 "Никаких сомнений",
                 "Может быть, я не знаю, я же шар",
                 "Слишком геморно, напиши позже",
                 "Лучше тебе не знать ответ на этот вопрос",
                 "Я настолько преисполнился в своём познании, что не хочу тебе отвечать",
                 "Ты уверен, что хочешь услышать ответ на это?",
                 "Нельзя просто так взять и ответить на этот вопрос",
                 "Ты хоть понимаешь, что спрашиваешь?",
                 "Может быть",
                 "┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻",
                 "Я бы ответил, но ответ настолько очевиден, что я не буду подсказывать",
                 "Мне так не кажется",
                 "Весьма сомнительно",
                 "В перспективе - да",
                 "Ебанутый ты задаёшь в ебанутом мире ебанутые вопросы ебанутому мне, чтобы получить ебанутый ответ?",
                 "Ебать мой лысый хуй, ты что, совсем, что ли, что за вопросы?",
                 "Мне кажется, задавая такие вопросы, ты хочешь получить пизды, причём в плохом смысле",
                 'Говорю "да" только потому что ты хочешь это услышать',
                 "Может быть. А, может, и нет. А, может, пошёл ты"
                 ]
        embed = discord.Embed(color=0x5B3375, description=f'{args} \n '
                                                          f'Ответ: {random.choice(responses)}')
        await context.send(embed=embed)

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        embed = discord.Embed(
            description=args,
        )
        await context.send(embed=embed)

    @commands.command(help='адм.команда-удаление сообщений')
    @commands.has_permissions(administrator=True)
    async def clear(self, context, num):
        msg = []  # Empty list to put all the messages in the log
        num = int(num)  # Converting the amount of messages to delete to an integer
        async for x in abc.Messageable.history(context.message.channel, limit=num):
            msg.append(x)
        await context.channel.delete_messages(msg)
        embed = discord.Embed(color=0x5B3375, description=f"{num} сообщений было удалено")
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
