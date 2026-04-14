import os
os.system("pip install -r requirements.txt")

import asyncio
import traceback
from threading import Thread
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands

from core import Context
from core.Cog import Cog
from core.synthx import synthx
from utils.Tools import *
from utils.config import *

import jishaku
import cogs

# ───────────────────────────────
#  Jishaku Env Settings
# ───────────────────────────────
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "False"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")

client = synthx()
tree = client.tree

# ─────────────────────────────────────
#  On Ready Event
# ─────────────────────────────────────
@client.event
async def on_ready():
    await client.wait_until_ready()
    print("\033[1;31mBot Started !\033[0m")
    print("Loaded & Online!")
    print(f"Logged in as: {client.user}")
    print(f"Connected to: {len(client.guilds)} guilds")
    print(f"Connected to: {len(client.users)} users")

    try:
        synced = await client.tree.sync()
        all_commands = list(client.commands)
        print(f"Synced Total {len(all_commands)} Client Commands and {len(synced)} Slash Commands")
    except Exception as e:
        print(e)

# ──────────────────────────────────────────────
#  Command Completion Webhook Logger
# ──────────────────────────────────────────────
@client.event
async def on_command_completion(context: commands.Context) -> None:
    if context.author.id == 767979794411028491:
        return

    full_command_name = context.command.qualified_name
    executed_command = str(full_command_name.split("\n")[0])
    webhook_url = "https://discord.com/api/webhooks/1473731603531563141/wzH1jRLDrkVd8UEsacRD1b_E171OkZg_4z4ZifNiHbzcmzlc1U-BJ_hg5WuHjwqNxQRc"

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)

        avatar_url = context.author.avatar.url if context.author.avatar else context.author.default_avatar.url
        embed = discord.Embed(color=0x000000)
        embed.set_author(
            name=f"Executed {executed_command} Command By : {context.author}",
            icon_url=avatar_url
        )
        embed.set_thumbnail(url=avatar_url)
        embed.add_field(name="Command Name", value=executed_command, inline=False)
        embed.add_field(
            name="Command Executed By",
            value=f"{context.author} | ID: [{context.author.id}](https://discord.com/users/{context.author.id})",
            inline=False
        )

        if context.guild:
            embed.add_field(
                name="Command Executed In",
                value=f"{context.guild.name} | ID: [{context.guild.id}](https://discord.com/guilds/{context.guild.id})",
                inline=False
            )
            embed.add_field(
                name="Command Executed In Channel",
                value=f"{context.channel.name} | ID: [{context.channel.id}](https://discord.com/channels/{context.guild.id}/{context.channel.id})",
                inline=False
            )

        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text="SynthX Development™", icon_url=client.user.display_avatar.url)
        try:
            await webhook.send(embed=embed)
        except Exception as e:
            print(f'Webhook failed: {e}')
            traceback.print_exc()

# ───────────────────────────────────
# 📌 Keep Alive Web Server (Replit / UptimeRobot)
# ───────────────────────────────────
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "SynthX Development™ 2025"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()

# ───────────────────────────────────
# Bot Startup
# ──────────────────────────────────
async def main():
    async with client:
        os.system("clear")
        # Load Extensions
        await client.load_extension("jishaku")
        await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())