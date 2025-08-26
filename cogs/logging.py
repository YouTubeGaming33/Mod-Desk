import discord
from discord.ext import commands
from discord import app_commands

from data.database import get_guild

class Logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.add_listener(self.on_moderation)

    async def on_moderation(self, interaction: discord.Interaction, target: discord.Member, action: str, reason: str):
        if action == "kick":
            print("Hello there")

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))