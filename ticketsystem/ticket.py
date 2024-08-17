import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_category_name = "Tickets"
        self.closed_ticket_category_name = "Geschlossene Tickets"

    @app_commands.command(name="startticket", description="Sendet ein Embed zum Erstellen eines Tickets.")
    async def start_ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Ticket-System", description="Eröffne hier ein Ticket:", color=0x00ff00)
        button = Button(label="Ticket erstellen", style=discord.ButtonStyle.green)

        async def button_callback(interaction: discord.Interaction):
            await self.create_ticket(interaction)

        button.callback = button_callback
        view = View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view)

    async def create_ticket(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name=self.ticket_category_name)

        if category is None:
            category = await guild.create_category(self.ticket_category_name)

        channel = await guild.create_text_channel(f'ticket-{interaction.user.name}', category=category)

        await channel.set_permissions(guild.default_role, read_messages=False)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        mod_role = discord.utils.get(guild.roles, name="Moderator")
        if mod_role:
            await channel.set_permissions(mod_role, read_messages=True, send_messages=True)

        embed = discord.Embed(title="Ticket", description=f"Erstellt von {interaction.user.mention}\nWähle aus den unten stehenden Buttons dein Anliegen aus:", color=0x00ff00)

        support_button = Button(label="Support", style=discord.ButtonStyle.blurple)
        report_button = Button(label="Report", style=discord.ButtonStyle.red)
        apply_button = Button(label="Bewerben", style=discord.ButtonStyle.green)

        async def handle_selection(interaction: discord.Interaction, category_name: str):
            await interaction.response.send_message(f"Du hast {category_name} ausgewählt.", ephemeral=True)
            await interaction.message.delete()

            new_embed = discord.Embed(title=f"{category_name}-Ticket", description=f"Erstellt von {interaction.user.mention}", color=0x00ff00)
            close_button = Button(label="Schließen", style=discord.ButtonStyle.red)

            async def close_callback(interaction: discord.Interaction):
                closed_category = discord.utils.get(guild.categories, name=self.closed_ticket_category_name)
                if closed_category is None:
                    closed_category = await guild.create_category(self.closed_ticket_category_name)

                await channel.set_permissions(interaction.user, read_messages=False, send_messages=False)
                await channel.edit(category=closed_category, name=f"geschlossen-{channel.name}")
                await interaction.response.send_message("Ticket wurde geschlossen und verschoben.", ephemeral=True)

            close_button.callback = close_callback
            close_view = View()
            close_view.add_item(close_button)

            await channel.send(embed=new_embed, view=close_view)

        support_button.callback = lambda interaction: handle_selection(interaction, "Support")
        report_button.callback = lambda interaction: handle_selection(interaction, "Report")
        apply_button.callback = lambda interaction: handle_selection(interaction, "Bewerben")

        view = View()
        view.add_item(support_button)
        view.add_item(report_button)
        view.add_item(apply_button)

        await channel.send(f'{interaction.user.mention} hat ein Ticket erstellt.', embed=embed, view=view)
        await interaction.response.send_message(f"Ticket wurde erstellt: {channel.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
