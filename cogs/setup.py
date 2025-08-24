# Import Required Discord Libary and Import(s).
import discord
from discord.ext import commands
from discord import app_commands

from data.database import add_guild

class SetupContainer(discord.ui.Container):
    title = discord.ui.TextDisplay("# Mod-Desk Setup")
    belowtitle = discord.ui.TextDisplay("Run the following Commands to Adjust your Server Specifc Settings")

    gap = discord.ui.Separator()

    command1 = discord.ui.TextDisplay("## /settings config")

class SetupView(discord.ui.LayoutView):
    container = SetupContainer(accent_color=0x7289da)

class MyContainer(discord.ui.Container):
    text = discord.ui.TextDisplay("# Thank you for adding Mod-Desk to your Server!")
    text1 = discord.ui.TextDisplay("Click one of the Following Buttons for Help with Setup and Usage")
    
    action_row = discord.ui.ActionRow()

    @action_row.button(label="Setup")
    async def setup_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            add_guild(interaction.guild.id)
            await interaction.response.send_message(view=SetupView())
        else:
            await interaction.response.send_message("You are not Authorised to use this, ask an Admin.", ephemeral=True)
    
    @action_row.button(label="Usage")
    async def usage_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Clicked1", ephemeral=True)
        else:
            await interaction.response.send_message("You are not Authorised to use this, ask an Admin.", ephemeral=True)
            
class WelcomeMessage(discord.ui.LayoutView):
    container = MyContainer(accent_color=0x7289da)

# Class for Setup Cog.
class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = guild.system_channel
        if not channel:
            print("⚠️ No system channel found.")
            return

        view = WelcomeMessage()
        await channel.send(view=view)

# Adds Cog to Mod-Desk Bot Class.
async def setup(bot):
    await bot.add_cog(Setup(bot))