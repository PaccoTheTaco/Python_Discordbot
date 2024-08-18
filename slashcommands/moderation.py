import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bannt einen Benutzer vom Server")
    @app_commands.describe(user="Der Benutzer, der gebannt werden soll", reason="Grund für den Bann")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason: str = "Kein Grund angegeben"):
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(f"{user.mention} wurde gebannt. Grund: {reason}", ephemeral=True)

    @app_commands.command(name="kick", description="Kickt einen Benutzer vom Server")
    @app_commands.describe(user="Der Benutzer, der gekickt werden soll", reason="Grund für den Kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.User, reason: str = "Kein Grund angegeben"):
        await interaction.guild.kick(user, reason=reason)
        await interaction.response.send_message(f"{user.mention} wurde gekickt. Grund: {reason}", ephemeral=True)

    @app_commands.command(name="mute", description="Stummt einen Benutzer für eine bestimmte Zeit")
    @app_commands.describe(user="Der Benutzer, der stummgeschaltet werden soll", time="Zeit in Minuten")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, user: discord.Member, time: int):
        mute_duration = timedelta(minutes=time)
        try:
            await user.timeout(mute_duration)
            await interaction.response.send_message(f"{user.mention} wurde für {time} Minuten stummgeschaltet.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Fehler beim Stummschalten von {user.mention}: {e}", ephemeral=True)

    @app_commands.command(name="warn", description="Verwarnt einen Benutzer")
    @app_commands.describe(user="Der Benutzer, der verwarnt werden soll", reason="Grund für die Verwarnung")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.User, reason: str = "Kein Grund angegeben"):
        await interaction.response.send_message(f"{user.mention} wurde verwarnt. Grund: {reason}", ephemeral=True)

    @app_commands.command(name="unban", description="Entbannt einen Benutzer vom Server")
    @app_commands.describe(username="Der Name des Benutzers, der entbannt werden soll")
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, username: str):
        try:
            banned_users = [entry async for entry in interaction.guild.bans()]
            user = discord.utils.find(lambda u: u.user.name == username, banned_users)
            
            if user:
                await interaction.guild.unban(user.user)
                await interaction.response.send_message(f"{user.user.mention} wurde entbannt.", ephemeral=True)
            else:
                await interaction.response.send_message(f"Benutzer mit dem Namen {username} nicht gefunden.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Fehler beim Entbannen des Benutzers {username}: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
