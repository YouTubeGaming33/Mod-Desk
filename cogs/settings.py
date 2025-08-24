import discord
from discord.ext import commands
from discord import app_commands
from data.database import get_guild, toggle_guild_setting

class ToggleButton(discord.ui.Button):
    def __init__(self, setting_name: str, state: bool):
        self.setting_name = setting_name
        label = "ON" if state else "OFF"
        style = discord.ButtonStyle.success if state else discord.ButtonStyle.danger

        super().__init__(label=label, style=style, custom_id=f"toggle_{setting_name}")

    async def callback(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id

        from data.database import toggle_guild_setting, get_guild
        toggle_guild_setting(guild_id, self.setting_name)

        guild_data = get_guild(guild_id)
        new_state = bool(guild_data[self.setting_name])

        # update button
        self.label = "ON" if new_state else "OFF"
        self.style = discord.ButtonStyle.success if new_state else discord.ButtonStyle.danger

        # 👇 make sure we *always* respond
        if interaction.response.is_done():
            await interaction.edit_original_response(view=self.view)
        else:
            await interaction.response.edit_message(view=self.view)

from discord.ui import Section, TextDisplay, Container

def make_settings_container(guild_data: dict):
    # Create the TextDisplay
    header = TextDisplay("# Configuration Dashboard")

    text = TextDisplay("👋 Welcome Messages")

    # Create the toggle button
    button = ToggleButton("welcome_enabled", guild_data["welcome_enabled"])


    text1 = TextDisplay("Logging")

    button1 = ToggleButton("logging_enabled", guild_data["logging_enabled"])

    section1 = Section(text1, accessory=button1)
    # Create the section with the button as accessory
    section = Section(text, accessory=button)

    # Put the section into a container
    container = discord.ui.Container()
    container.add_item(header)
    container.add_item(section)
    container.add_item(section1)
    return container


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    settings = app_commands.Group(name="settings", description="Guild settings")

    @settings.command(name="config")
    async def config(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)  # 👈 important
        try:
            guild_data = get_guild(interaction.guild.id)
            container = make_settings_container(guild_data)
            view = discord.ui.LayoutView()
            view.add_item(container)
            await interaction.followup.send(view=view, ephemeral=True)
        except Exception as e:
            print (e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))
