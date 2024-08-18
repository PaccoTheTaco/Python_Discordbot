import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
import re

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_giveaways = {}

    @commands.hybrid_command(name="startgiveaway")
    async def start_giveaway(self, ctx, title: str, prize: str, emoji: str, duration: str):
        if not self.is_valid_emoji(emoji, ctx.guild):
            await ctx.send("Ungültiges Emoji. Bitte wähle ein gültiges Emoji.", ephemeral=True)
            return

        try:
            end_time = datetime.now() + self.parse_duration(duration)
        except ValueError:
            await ctx.send("Ungültiges Zeitformat. Bitte verwende z.B. 1h, 30m, 2d.", ephemeral=True)
            return
        
        end_timestamp = int(end_time.timestamp())

        embed = discord.Embed(
            title=f"{title}", 
            description=(
                f"Preis: **{prize}**\n"
                f"Reagiere mit {emoji} um teilzunehmen!\n\n"
                f"Endet am <t:{end_timestamp}:F> (<t:{end_timestamp}:R>)"
            ),
            color=discord.Color.blue()
        )
        giveaway_message = await ctx.send(embed=embed)
        await giveaway_message.add_reaction(emoji)
        
        self.active_giveaways[giveaway_message.id] = {
            "title": title,
            "prize": prize,
            "emoji": emoji,
            "participants": [],
            "end_time": end_time
        }

        self.bot.loop.create_task(self.wait_for_giveaway_end(ctx, giveaway_message.id, end_time))

    async def wait_for_giveaway_end(self, ctx, message_id, end_time):
        await asyncio.sleep((end_time - datetime.now()).total_seconds())
        if message_id in self.active_giveaways:
            await self.complete_giveaway(ctx, message_id)

    async def complete_giveaway(self, ctx, message_id):
        giveaway = self.active_giveaways.pop(message_id, None)
        if giveaway:
            participants = giveaway["participants"]
            if participants:
                winner = random.choice(participants)
                embed = discord.Embed(
                    title="🎉 Giveaway Beendet! 🎉",
                    description=f"**{giveaway['title']}**\n\nPreis: **{giveaway['prize']}**",
                    color=discord.Color.gold()
                )
                embed.add_field(name="Gewinner", value=f"{winner.mention}", inline=False)
                embed.set_footer(text="Danke an alle, die teilgenommen haben!")
                embed.set_thumbnail(url=winner.avatar.url if winner.avatar else None)
                embed.set_image(url="https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="🎉 Giveaway Beendet! 🎉",
                    description=f"**{giveaway['title']}**\n\nPreis: **{giveaway['prize']}**",
                    color=discord.Color.red()
                )
                embed.add_field(name="Kein Gewinner", value="Leider hat niemand teilgenommen.", inline=False)
                embed.set_footer(text="Vielleicht beim nächsten Mal!")
                await ctx.send(embed=embed)
        else:
            await ctx.send("Es gab ein Problem beim Beenden des Giveaways.", ephemeral=True)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        
        message_id = reaction.message.id
        emoji = reaction.emoji

        if message_id in self.active_giveaways:
            giveaway = self.active_giveaways[message_id]
            if str(emoji) == giveaway["emoji"]:
                if user not in giveaway["participants"]:
                    giveaway["participants"].append(user)

    @staticmethod
    def is_valid_emoji(emoji: str, guild: discord.Guild) -> bool:
        standard_emoji_pattern = r'^[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+$'
        if re.match(standard_emoji_pattern, emoji):
            return True
        
        for custom_emoji in guild.emojis:
            if f"<:{custom_emoji.name}:{custom_emoji.id}>" == emoji or f"<a:{custom_emoji.name}:{custom_emoji.id}>" == emoji:
                return True
        
        return False

    @staticmethod
    def parse_duration(duration: str) -> timedelta:
        unit = duration[-1]
        amount = int(duration[:-1])
        if unit == 's':
            return timedelta(seconds=amount)
        elif unit == 'm':
            return timedelta(minutes=amount)
        elif unit == 'h':
            return timedelta(hours=amount)
        elif unit == 'd':
            return timedelta(days=amount)
        else:
            raise ValueError("Invalid time unit")

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
