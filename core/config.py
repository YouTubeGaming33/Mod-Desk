# Required Library(s)
import os
import discord

from dotenv import load_dotenv

# Pulls Discord Token from .env - includes Loading.
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GMAIL_PASSWORD = os.getenv("GMAIL_PASS")

# Variable for GUILD ID - Development Purposes.
GUILD_ID = discord.Object(id=1408216142648184852)