import discord
from discord.ext import commands
import os
import discord
from discord.ext import commands
from discord import abc
import requests
import random
import datetime
import asyncio
from bs4 import BeautifulSoup as bs


headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 YaBrowser/19.9.0.1343 Yowser/2.5 Safari/537.36'}
base_url = 'https://pikabu.ru/community/steam'


class inWork(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Команда поиска картинки по слову')
    async def pic(ctx, keyword):
        author = ctx.message.author
        await ctx.send(f'{author.mention}, ищу картиночку, ожидайте...', delete_after=3)
        response = requests.get('https://source.unsplash.com/1600x900/?'+keyword)  # Get-запрос
        embed = discord.Embed(color=0x5B3375)  # Создание Embed'a
        embed.set_image(url=response.url)  # Устанавливаем картинку Embed'a
        await ctx.send(embed=embed)  # Отправляем Embed

    @commands.command(help='Команда поиска рандомной картинки')
    async def randompic(ctx):
        author = ctx.message.author
        await ctx.send(f'{author.mention}, ищу картиночку, ожидайте...', delete_after=3)
        response = requests.get('https://source.unsplash.com/1600x900/')  # Get-запрос
        embed = discord.Embed(color=0x5B3375)  # Создание Embed'a
        embed.set_image(url=response.url)  # Устанавливаем картинку Embed'a
        await ctx.send(embed=embed)  # Отправляем Embed

    @commands.command(help='адм.команда-добавление роли юзеру')
    @commands.has_permissions(administrator=True)
    async def addrole(ctx, user: discord.Member, role: discord.Role):
        await user.add_roles(role)
        embed = discord.Embed(color=0x5B3375, description=f"Юзеру {user.mention} была выдана роль: {role.mention}")
        await ctx.send(embed=embed)

    @commands.command(help='адм.команда-удаление роли юзера')
    @commands.has_permissions(administrator=True)
    async def removerole(ctx, user: discord.Member, role: discord.Role):
        await user.remove_roles(role)
        embed = discord.Embed(color=0x5B3375, description=f"С юзера {user.mention} была снята роль: {role.mention}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def chnick(ctx, member: discord.Member, *, nick):
        try:
            await member.edit(nick=nick)
            embed = discord.Embed(color=0x5B3375, description=f'Никнейм был изменён на {member.mention} ')
            await ctx.send(embed=embed)
        except discord.ext.commands.errors.MissingPermissions(administrator=True):
            embed = discord.Embed(color=0x5B3375, description='У тебя нет здесь власти!')
            await ctx.send(embed=embed)

    @commands.command(help='create-channel')
    async def create_channel(ctx):
        guild = ctx.guild
        author = ctx.message.author
        channel_name = author+'s channel'
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            embed = discord.Embed(color=0x5B3375, description=f'Creating a new channel: {channel_name}')
            await ctx.send(embed=embed)
            await guild.create_voice_channel(channel_name)

    # Voice mute and unmute
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mutev(ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Voice')
        await member.add_roles(mute_role)
        await member.edit(mute=True, deafen=True)
        await ctx.send(f'{member.mention} получил мут за плохое поведение!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmutev(ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Voice')
        await member.remove_roles(mute_role)
        await member.edit(mute=False, deafen=False)
        await ctx.send(f'{member.mention} размьючен!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mutec(ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Chat')
        await member.add_roles(mute_role)
        await member.edit(deafen=True)
        await ctx.send(f'{member.mention} получил мут за плохое поведение!')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmutec(ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted Chat')
        await member.remove_roles(mute_role)
        await member.edit(deafen=False)
        await ctx.send(f'{member.mention} размьючен!')


def setup(bot):
    bot.add_cog(inWork(bot))
