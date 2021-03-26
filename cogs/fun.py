import os, sys, discord, random, asyncio
from discord.ext import commands


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dick")
    async def dick(self, context, member: discord.Member = None):
        """
        Get the dick's length of a user or yourself.
        """
        if not member:
            member = context.author
        length = random.randrange(15)
        embed = discord.Embed(description=f"8{'='*length}D")
        embed.set_author(name=f"{member.display_name}'s Dick", icon_url=member.avatar_url)
        await context.send(embed=embed)

    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        choices = {
            0 : "rock",
            1 : "paper",
            2 : "scissors"
        }
        reactions = {
            "🪨" : 0,
            "🧻" : 1,
            "✂" : 2
        }
        embed = discord.Embed(title="Please choose")
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed()
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Too late")
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)

    @commands.command(name="beer")
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(name="slot")
    async def slot(self, context):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{context.author.name}**,"

        if (a == b == c):
            await context.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await context.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await context.send(f"{slotmachine} No match, you lost 😢")

def setup(bot):
    bot.add_cog(Fun(bot))
