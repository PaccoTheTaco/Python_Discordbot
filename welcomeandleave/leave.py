import discord
from discord.ext import commands

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_id = 1261639102227546134
        
        channel = self.bot.get_channel(channel_id)
        
        if channel is not None:
            embed = discord.Embed(
                title=f"{member.name} hat den Server verlassen",
                description="Wir werden dich vermissen!\nHoffentlich sehen wir dich bald wieder!",
                color=discord.Color.red() 
            )
            embed.set_thumbnail(url=member.avatar.url)  
            
            await channel.send(embed=embed)
        else:
            print(f"Kanal mit der ID {channel_id} wurde nicht gefunden.")

async def setup(bot):
    await bot.add_cog(Leave(bot))
