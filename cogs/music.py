import discord
from discord.ext import commands
import discord
from discord.ext import commands
from discord import abc
import requests
import random
import datetime
import asyncio
from bs4 import BeautifulSoup as bs


class Music(commands.Cog, name="music"):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
    # async def join(self, ctx):
    #     channel = ctx.message.author.voice.channel
    #     if not channel:
    #         await ctx.send("You are not connected to a voice channel")
    #         return
    #     voice = get(self.voice_clients, guild=ctx.guild)
    #     if voice and voice.is_connected():
    #         await voice.move_to(channel)
    #     else:
    #         voice = await channel.connect()
    #     await voice.disconnect()
    #     if voice and voice.is_connected():
    #         await voice.move_to(channel)
    #     else:
    #         voice = await channel.connect()
    #     await ctx.send(f"Joined {channel}")

    # @commands.command(name="join")
    # async def join(self, context):
    #     global voice
    #     channel = context.message.author.voice.channel
    #     voice = context.get(commands.voice_clients, guild=context.guild)
    #
    #     if voice and voice.is_connected():
    #         await voice.move_to(channel)
    #     else:
    #         voice = await channel.connect()
    #         await context.send('успешно подключился')
    #
    # @commands.command(name="leave")
    # async def leave(self, context):
    #     global voice
    #     channel = context.message.author.voice.channel
    #     voice = context.get(commands.voice_clients, guild=context.guild)
    #
    #     if voice and voice.is_connected():
    #         await voice.disconnect()
    #     else:
    #         voice = await channel.disconnect()
    #         await context.send('успешно отключился')


def setup(bot):
    bot.add_cog(Music(bot))
