import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot ist eingeloggt als {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Slash-Commands synchronisiert: {len(synced)} Befehle")
    except Exception as e:
        print(f"Fehler beim Synchronisieren der Slash-Commands: {e}")

async def load_extensions():
    await bot.load_extension("slashcommands.ping")

async def main():
    await load_extensions()
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())
