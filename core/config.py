# Required Library(s)
import os
import discord

# Pulls Discord Token from .env - If not found then Raises Error.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Variable for GUILD ID - Development Purposes.
GUILD_ID = discord.Object(id=1381317351211008051)