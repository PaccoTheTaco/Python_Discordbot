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
        if before.author.bot or before.content == after.content:
            return
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

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        log_channel_id = 1261650197058945077
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            if before.nick != after.nick:
                embed = discord.Embed(
                    title="Nickname geändert",
                    color=discord.Color.blue(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="User", value=after.mention, inline=False)
                embed.add_field(name="Vorher", value=before.nick if before.nick else "Kein Nickname", inline=False)
                embed.add_field(name="Nachher", value=after.nick if after.nick else "Kein Nickname", inline=False)
                await log_channel.send(embed=embed)

            before_roles = set(before.roles)
            after_roles = set(after.roles)
            added_roles = after_roles - before_roles
            removed_roles = before_roles - after_roles

            if added_roles:
                for role in added_roles:
                    embed = discord.Embed(
                        title="Rolle hinzugefügt",
                        color=discord.Color.green(),
                        timestamp=discord.utils.utcnow()
                    )
                    embed.add_field(name="User", value=after.mention, inline=False)
                    embed.add_field(name="Rolle", value=role.name, inline=False)
                    await log_channel.send(embed=embed)

            if removed_roles:
                for role in removed_roles:
                    embed = discord.Embed(
                        title="Rolle entfernt",
                        color=discord.Color.red(),
                        timestamp=discord.utils.utcnow()
                    )
                    embed.add_field(name="User", value=after.mention, inline=False)
                    embed.add_field(name="Rolle", value=role.name, inline=False)
                    await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        log_channel_id = 1261650197058945077
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            if before.name != after.name:
                embed = discord.Embed(
                    title="Username geändert",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="Vorher", value=before.name, inline=False)
                embed.add_field(name="Nachher", value=after.name, inline=False)
                embed.set_footer(text=f"User ID: {after.id}")
                await log_channel.send(embed=embed)

            if before.avatar != after.avatar:
                embed = discord.Embed(
                    title="Avatar geändert",
                    color=discord.Color.blue(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="User", value=after.mention, inline=False)
                embed.set_thumbnail(url=before.avatar.url if before.avatar else "")
                embed.set_image(url=after.avatar.url if after.avatar else "")
                embed.set_footer(text=f"User ID: {after.id}")
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel_id = 1261650197058945077
        log_channel = self.bot.get_channel(log_channel_id)
        if not log_channel:
            return
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(
                title="Voice-Channel beigetreten",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Channel", value=after.channel.name, inline=False)
            await log_channel.send(embed=embed)
        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(
                title="Voice-Channel verlassen",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Channel", value=before.channel.name, inline=False)
            await log_channel.send(embed=embed)
        elif before.channel is not None and after.channel is not None and before.channel.id != after.channel.id:
            embed = discord.Embed(
                title="Voice-Channel gewechselt",
                color=discord.Color.orange(),
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="User", value=member.mention, inline=False)
            embed.add_field(name="Von Channel", value=before.channel.name, inline=True)
            embed.add_field(name="Zu Channel", value=after.channel.name, inline=True)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel_id = 1261650197058945077
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="Rolle erstellt",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="Rolle", value=role.name, inline=False)
            embed.add_field(name="Rollen-ID", value=role.id, inline=False)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel_id = 1261650197058945077
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="Rolle gelöscht",
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            embed.add_field(name="Rolle", value=role.name, inline=False)
            embed.add_field(name="Rollen-ID", value=role.id, inline=False)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        log_channel_id = 1261650197058945077
        log_channel = self.bot.get_channel(log_channel_id)
        if log_channel:
            if before.name != after.name:
                embed = discord.Embed(
                    title="Rollenname geändert",
                    color=discord.Color.blue(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="Vorher", value=before.name, inline=False)
                embed.add_field(name="Nachher", value=after.name, inline=False)
                embed.add_field(name="Rollen-ID", value=after.id, inline=False)
                await log_channel.send(embed=embed)
            if before.permissions != after.permissions:
                embed = discord.Embed(
                    title="Rollenberechtigungen geändert",
                    color=discord.Color.orange(),
                    timestamp=discord.utils.utcnow()
                )
                embed.add_field(name="Rolle", value=after.name, inline=False)
                embed.add_field(name="Rollen-ID", value=after.id, inline=False)
                before_perms = [perm[0] for perm in before.permissions if perm[1]]
                after_perms = [perm[0] for perm in after.permissions if perm[1]]
                added_perms = set(after_perms) - set(before_perms)
                removed_perms = set(before_perms) - set(after_perms)
                if added_perms:
                    embed.add_field(name="Hinzugefügte Berechtigungen", value=", ".join(added_perms), inline=False)
                if removed_perms:
                    embed.add_field(name="Entfernte Berechtigungen", value=", ".join(removed_perms), inline=False)
                await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
