import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_cache = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ist bereit und lädt Nachrichten-Historie...")
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit=100):
                        if message.id not in self.message_cache:
                            self.message_cache[message.id] = message
                except discord.Forbidden:
                    print(f"Keine Berechtigung zum Laden der Nachrichten-Historie in {channel.name}")
                except Exception as e:
                    print(f"Fehler beim Laden der Nachrichten-Historie in {channel.name}: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.id not in self.message_cache:
            self.message_cache[message.id] = message

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        cached_message = self.message_cache.get(message.id)
        if cached_message:
            log_channel_id = 1261650197058945077
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                embed = discord.Embed(
                    title="Nachricht gelöscht",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="User", value=cached_message.author.mention, inline=False)
                embed.add_field(name="Nachricht", value=cached_message.content if cached_message.content else "Kein Text", inline=False)
                embed.set_footer(text=f"Nachricht ID: {cached_message.id}")

                await log_channel.send(embed=embed)
            del self.message_cache[message.id]

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.id in self.message_cache:
            self.message_cache[before.id] = after

        log_channel_id = 1261650197058945077
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="Nachricht bearbeitet",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="User", value=before.author.mention, inline=False)
            embed.add_field(name="Nachricht vorher", value=before.content if before.content else "Kein Text", inline=False)
            embed.add_field(name="Nachricht nachher", value=after.content if after.content else "Kein Text", inline=False)
            embed.set_footer(text=f"Nachricht ID: {before.id}")

            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
