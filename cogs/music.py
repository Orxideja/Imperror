from discord.ext import commands


class Music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join")
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = ctx.get(commands.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send('успешно подключился')

    @commands.command(name="leave")
    async def leave(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = ctx.get(commands.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            voice = await channel.disconnect()
            await ctx.send('успешно отключился')


def setup(bot):
    bot.add_cog(Music(bot))
