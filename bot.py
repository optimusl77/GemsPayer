import discord
import re
import asyncio
import json
from discord.ext import commands


TOKEN = "YOUR TOKEN"
CHANNELS_FILE = "channels.json"

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

balance_check_interval = 60
balance_channels = set()


def save_channels():
    with open(CHANNELS_FILE, "w") as f:
        json.dump(list(balance_channels), f)


def load_channels():
    global balance_channels
    try:
        with open(CHANNELS_FILE, "r") as f:
            balance_channels = set(json.load(f))
    except FileNotFoundError:
        balance_channels = set()


@client.event
async def on_ready():
    load_channels()
    client.loop.create_task(balance_loop())


async def balance_loop():
    while True:
        await asyncio.sleep(balance_check_interval)
        for channel_id in balance_channels:
            channel = client.get_channel(channel_id)
            if channel:
                await channel.send("/gems balance")


@client.command()
async def time(ctx, seconds: int = None):
    global balance_check_interval
    if seconds is None:
        await ctx.send(f"Cooldown:`{balance_check_interval}` sek.")
        return
    balance_check_interval = seconds
    await ctx.send(f"Intervall für /gems balance auf **{seconds}** Sekunden gesetzt.")



client.remove_command("help")
@client.command(name="help")
async def commands_list(ctx):
    commands_info = {
        "!time <Sekunden>": "Setzt das Intervall für /gems balance.",
        "!setchannel add": "Fügt den aktuellen Kanal für automatische /gems balance Abfragen hinzu.",
        "!setchannel add <Kanal-ID>": "Fügt einen spezifischen Kanal für automatische /gems balance Abfragen hinzu.",
        "!setchannel del": "Entfernt den aktuellen Kanal von den automatischen /gems balance Abfragen.",
        "!setchannel del <Kanal-ID>": "Entfernt einen spezifischen Kanal von den automatischen /gems balance Abfragen.",
        "!setchannel": "Listet alle registrierten Kanäle auf.",
    }

    help_message = "**📜 Verfügbare Befehle:**\n" + "\n".join(
        [f"`{cmd}` - {desc}" for cmd, desc in commands_info.items()])

    await ctx.send(help_message)


@client.command()
async def setchannel(ctx, action: str = None, channel_id: int = None):
    global balance_channels

    if action is None:
        if not balance_channels:
            await ctx.send("Es sind keine Kanäle registriert.")
        else:
            channel_mentions = [f"<#{channel_id}>" for channel_id in balance_channels]
            channel_list = "\n".join(channel_mentions)
            await ctx.send(f"**Registrierte Kanäle:**\n{channel_list}")
        return

    if action.lower() == "add":
        if channel_id:
            channel = client.get_channel(channel_id)
            if channel:
                balance_channels.add(channel_id)
                save_channels()
                await ctx.send(f"Der Kanal <#{channel_id}> wurde für automatische /gems balance Abfragen hinzugefügt.")
            else:
                await ctx.send("Ungültige Kanal-ID! Stelle sicher, dass der Bot Zugriff auf den Kanal hat.")
        else:  # Falls keine ID angegeben wurde, nimm den aktuellen Kanal
            balance_channels.add(ctx.channel.id)
            save_channels()
            await ctx.send("Dieser Kanal wurde für automatische /gems balance Abfragen hinzugefügt.")

    elif action.lower() == "del":
        if channel_id:
            if channel_id in balance_channels:
                balance_channels.remove(channel_id)
                save_channels()
                await ctx.send(f"Der Kanal <#{channel_id}> wurde entfernt.")
            else:
                await ctx.send("Dieser Kanal war nicht registriert.")
        else:
            if ctx.channel.id in balance_channels:
                balance_channels.remove(ctx.channel.id)
                save_channels()
                await ctx.send("Dieser Kanal wurde entfernt.")
            else:
                await ctx.send("Dieser Kanal war nicht registriert.")

    else:
        await ctx.send("Ungültige Aktion! Verwende `!setchannel add [Kanal-ID]` oder `!setchannel del [Kanal-ID]`.")


@client.event
async def on_message(message):
    if message.content.startswith("."):
        return

    await client.process_commands(message)



@client.event
async def on_message(message):
    if message.channel.id in balance_channels:
        if message.embeds:
            for embed in message.embeds:
                embed_dict = embed.to_dict()
                embed_text = embed_dict.get("title", "") + " " + embed_dict.get("description", "")

                if "You have sent" in embed_text:
                    return

                match = re.search(r'(\d{1,})\s*gems', embed_text, re.IGNORECASE)
                if match:
                    gems_amount = match.group(1)
                    await message.channel.send(f"/gems pay 9w9w {gems_amount}")
                    return

        match = re.search(r'(\d{1,})\s*gems', message.content, re.IGNORECASE)
        if match:
            gems_amount = match.group(1)
            await message.channel.send(f"/gems pay 9w9w {gems_amount}")
            return

    await client.process_commands(message)


client.run(TOKEN)