import discord
from mcrcon import MCRcon
import traceback
import time
import asyncio

# ---------------- CONFIG ----------------
CONFIG = {
    "General": {
        # Put the channel ID where you want the bot to listen
        "DiscordChannelID": 123456789012345678,  # <-- REPLACE ME

        # Prefix shown in ARK chat
        "DiscordSenderPrefix": "[Discord]",

        # Your Discord bot token (keep private)
        "BotToken": "YOUR_DISCORD_BOT_TOKEN_HERE"
    },
    "Rcon": {
        # Replace these with your server details
        "The Island": {"Host": "127.0.0.1", "Port": 27020, "Password": "YOUR_RCON_PASSWORD_HERE"},
        "Ragnarok": {"Host": "127.0.0.1", "Port": 27021, "Password": "YOUR_RCON_PASSWORD_HERE"},
        "Scorched Earth": {"Host": "127.0.0.1", "Port": 27022, "Password": "YOUR_RCON_PASSWORD_HERE"},
        "The Center": {"Host": "127.0.0.1", "Port": 27023, "Password": "YOUR_RCON_PASSWORD_HERE"},
        "Aberration": {"Host": "127.0.0.1", "Port": 27024, "Password": "YOUR_RCON_PASSWORD_HERE"},
        "Valguero": {"Host": "127.0.0.1", "Port": 27025, "Password": "YOUR_RCON_PASSWORD_HERE"},
        "Extinction": {"Host": "127.0.0.1", "Port": 27026, "Password": "YOUR_RCON_PASSWORD_HERE"}
    },

    # Blocks common mention spam
    "DiscordMsgFilters": ["@everyone", "@here"],

    # Optional: your Discord invite link for the /discord command
    # Leave as placeholder if you don't want it public.
    "DiscordInviteLink": "YOUR_DISCORD_INVITE_LINK_HERE"
}
# ----------------------------------------

DISCORD_CHANNEL_ID = CONFIG["General"]["DiscordChannelID"]
DISCORD_SENDER_PREFIX = CONFIG["General"]["DiscordSenderPrefix"]
DISCORD_TOKEN = CONFIG["General"]["BotToken"]
RCON_SERVERS = CONFIG["Rcon"]
FILTERS = CONFIG["DiscordMsgFilters"]
DISCORD_INVITE_LINK = CONFIG["DiscordInviteLink"]

discord_cooldowns = {}
COOLDOWN_SECONDS = 120

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    print("Listening for messages in channel:", DISCORD_CHANNEL_ID)

@client.event
async def on_message(message):
    try:
        if message.author.bot or message.channel.id != DISCORD_CHANNEL_ID:
            return

        # Command: /discord (posts invite link to ARK chat)
        if message.content.strip().lower() == "/discord":
            now = time.time()
            last_used = discord_cooldowns.get(message.author.id, 0)

            if now - last_used >= COOLDOWN_SECONDS:
                ark_msg = f"{DISCORD_SENDER_PREFIX} {message.author.display_name}: {DISCORD_INVITE_LINK}"

                for rcon_data in RCON_SERVERS.values():
                    try:
                        with MCRcon(rcon_data["Host"], rcon_data["Password"], port=rcon_data["Port"]) as mcr:
                            mcr.command(f"ServerChat {ark_msg}")
                    except Exception as e:
                        print(f"❌ Failed to send /discord link: {e}")

                discord_cooldowns[message.author.id] = now
            else:
                remaining = int(COOLDOWN_SECONDS - (now - last_used))
                await message.channel.send(f"⏱ Please wait {remaining} seconds before using /discord again.")
            return

        # Filter messages containing blocked patterns
        if any(f in message.content for f in FILTERS):
            return

        # Forward normal messages into ARK chat via RCON
        ark_msg = f"{DISCORD_SENDER_PREFIX} {message.author.display_name}: {message.content}"
        print(f"{message.author.display_name}: {message.content}")

        for rcon_data in RCON_SERVERS.values():
            try:
                with MCRcon(rcon_data["Host"], rcon_data["Password"], port=rcon_data["Port"]) as mcr:
                    mcr.command(f"ServerChat {ark_msg}")
            except Exception as e:
                print(f"❌ Failed to send message: {e}")

    except Exception as e:
        print(f"⚠️ Error in Discord message handler: {e}")
        traceback.print_exc()

async def main():
    await client.start(DISCORD_TOKEN)

try:
    asyncio.run(main())
except Exception as e:
    print(f"⚠️ Failed to start bot: {e}")
    traceback.print_exc()

print("\nPress ENTER to exit...")
input()
