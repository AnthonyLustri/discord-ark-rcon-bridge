# Discord to ARK RCON Bridge (Python)

A Python-based Discord bot that **forwards messages from a Discord channel into ARK server in-game chat** using RCON.

This project is designed for ARK communities that want seamless chat visibility between Discord and in-game players, with basic spam protection and command handling.

---

## ✨ Features

- 💬 Relays Discord messages directly into ARK in-game chat
- 🌐 Supports **multiple ARK servers at once**
- 🛑 Filters common mention spam (`@everyone`, `@here`)
- ⏱️ Cooldown-protected `/discord` command
- 🔐 Uses placeholders for secrets (safe for public repositories)
- ⚙️ Built with Python, `discord.py`, and RCON

---

## 🧠 What This Bot Does

This bot listens to **one specific Discord channel** and performs the following actions:

### Message Forwarding
- Normal Discord messages are forwarded to ARK in-game chat
- Messages are prefixed so players know they came from Discord
- Messages containing blocked patterns are ignored

### `/discord` Command
- When a user types `/discord`, the bot sends a Discord invite link into ARK chat
- The command is protected by a **per-user cooldown** to prevent spam

> ⚠️ This bot does **not** manage servers, start/stop services, or run WindowsGSM commands.  
> It only sends chat messages via RCON.

---

## 🔧 Requirements

- Python **3.9+**
- A Discord bot application
- Discord **Message Content Intent** enabled
- One or more ARK servers with **RCON enabled**
- Network access from the bot to your ARK servers

---

## 📦 Python Dependencies

Install required libraries:

```bash
pip install discord.py mcrcon
```

---

## ⚙️ Configuration

All configuration is handled in the `CONFIG` dictionary inside the script.

### Discord Settings

```python
"DiscordChannelID": 123456789012345678
"BotToken": "YOUR_DISCORD_BOT_TOKEN_HERE"
"DiscordSenderPrefix": "[Discord]"
```

- **DiscordChannelID** – The channel the bot listens to
- **BotToken** – Your Discord bot token (keep private)
- **DiscordSenderPrefix** – Prefix shown in ARK chat

---

### RCON Server Configuration

```python
"Server Name": {
    "Host": "127.0.0.1",
    "Port": 27020,
    "Password": "YOUR_RCON_PASSWORD_HERE"
}
```

- Add as many servers as needed
- Messages are broadcast to **all configured servers**

---

### Message Filters

```python
"DiscordMsgFilters": ["@everyone", "@here"]
```

Messages containing these strings will not be forwarded.

---

### Discord Invite Link (Optional)

Used by the `/discord` command:

```python
"DiscordInviteLink": "YOUR_DISCORD_INVITE_LINK_HERE"
```

---

## 🚀 Running the Bot

From the project directory:

```bash
python bot.py
```

On startup, the bot will:
1. Connect to Discord
2. Listen for messages in the configured channel
3. Forward messages to ARK servers via RCON

---

## 🛠️ Recommended Usage

- Run in a **screen**, **tmux**, or as a service
- Use a **dedicated Discord channel** for in-game chat
- Restrict bot permissions to only required channels
- Test RCON connectivity before long-term use

---

## ⚠️ Important Notes

- 🔐 Keep your **bot token and RCON passwords private**
- ⏱️ The `/discord` command uses a cooldown to prevent abuse
- 🧵 RCON connections are opened per message (by design)
- 🚫 Avoid enabling Discord mentions to prevent spam
- 🧪 Always test with one server before scaling up

---

## ❤️ Credits

Built for ARK server administrators who want reliable, real-time Discord-to-game chat using Python and RCON.
