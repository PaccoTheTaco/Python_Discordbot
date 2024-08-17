import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1261639082904387656
        
        channel = self.bot.get_channel(channel_id)
        
        if channel is not None:
            embed = discord.Embed(
                title=f"Willkommen, {member.mention}!",
                description="Schön, dass du da bist! Wir freuen uns, dich auf unserem Server begrüßen zu dürfen.",
                color=discord.Color.green() 
            )
            embed.set_thumbnail(url=member.avatar.url)  
            
            await channel.send(embed=embed)
        else:
            print(f"Kanal mit der ID {channel_id} wurde nicht gefunden.")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
