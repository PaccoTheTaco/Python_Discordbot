import discord
from discord import app_commands
from discord.ext import commands
import random
import requests

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Würfelt eine Zahl zwischen 1 und der angegebenen Zahl.")
    async def roll(self, interaction: discord.Interaction, number: int):
        result = random.randint(1, number)
        await interaction.response.send_message(f'🎲 Du hast eine {result} gewürfelt!')

    @app_commands.command(name="meme", description="Postet ein zufälliges Meme.")
    async def meme(self, interaction: discord.Interaction):
        meme_url = await self.get_random_meme()
        if meme_url:
            await interaction.response.send_message(meme_url)
        else:
            await interaction.response.send_message("Konnte kein Meme finden")

    async def get_random_meme(self):
        url = "https://meme-api.com/gimme"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('url')
        return None

    @app_commands.command(name="joke", description="Erzählt einen Witz.")
    async def joke(self, interaction: discord.Interaction):
        joke = await self.get_random_joke()
        if joke:
            await interaction.response.send_message(joke)
        else:
            await interaction.response.send_message("Konnte keinen Witz finden")

    async def get_random_joke(self):
        url = "https://official-joke-api.appspot.com/jokes/random"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f'{data["setup"]} - {data["punchline"]}'
        return None

    @app_commands.command(name="8ball", description="Beantwortet eine Frage im Magic-8-Ball-Stil.")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "Ja.", "Nein.", "Vielleicht.", "Frag später noch einmal.", "Es ist sicher.", "Sieht gut aus.",
            "Sehr zweifelhaft.", "Bestimmt nicht."
        ]
        answer = random.choice(responses)
        await interaction.response.send_message(f'🎱 {answer}')

async def setup(bot):
    await bot.add_cog(Fun(bot))
