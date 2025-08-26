import discord
from discord.ext import commands
from discord import app_commands

from typing import Optional

from data.database import get_guild

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    moderation = app_commands.Group(name="moderation", description="Moderation Commands")

    @moderation.command(name="kick", description="Kick a Member")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        if interaction.user.guild_permissions.moderate_members: # Checks for Permission to Moderate Members
            if member.id == interaction.user.id:
                await interaction.response.send_message("🚫 You can Not kick Yourself", ephemeral=True)
                return
            if member.top_role >= interaction.user.top_role: # Checks if Member is above Moderator using the Command
                await interaction.response.send_message("🚫 You can Not kick someone Above your Role", ephemeral=True)
                return
            if reason is None: # Checks for Reason, if None, defaults to "No Reason Provided"
                reason = "No Reason Provided"
            await interaction.response.send_message(f"{member.mention} has been Kicked for: **{reason}**", ephemeral=True)
            await member.kick(reason=reason)
            guildData = get_guild(interaction.guild.id)
            Logging = guildData["logging_enabled"]
            if Logging:
                self.bot.dispatch("moderation", interaction, member, "kick", reason)
        else:
            await interaction.response.send_message("🚫 You do not have Permission to Moderate Members.", ephemeral=True)

    @moderation.command(name="ban", description="Ban a Member")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = None):
        if interaction.user.guild_permissions.ban_members:
            if member.id == interaction.user.id:
                await interaction.response.send_message("🚫 You can Not ban Yourself", ephemeral=True)
                return
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message("🚫 You can Not Ban someone Above your Role", ephemeral=True)
                return
            if reason is None:
                reason = "No Reason Provided"
            await interaction.response.send_message(f"{member.mention} has been Banned for: **{reason}**", ephemeral=True)
            await member.ban(reason=reason)
        else:
            await interaction.response.send_message("🚫 You do not have Permission to Moderate Members.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))