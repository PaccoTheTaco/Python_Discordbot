import discord
from discord import app_commands
from discord.ext import commands

def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.administrator

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Zeigt die Latenzzeit des Bots an.")
    @app_commands.check(is_admin)
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000  
        await interaction.response.send_message(f"Pong! Latenz: {latency:.2f} ms 🏓")

    @ping.error
    async def ping_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
