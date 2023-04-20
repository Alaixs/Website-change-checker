import datetime
import discord
import requests
import pytz
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

url_discord = "WEBHOOK_HERE"
tz = pytz.timezone('Europe/Paris')

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def statut(ctx):
    with open('last_request_time.txt', 'r') as f:
        last_request_time_str = f.read()
    last_request_time = datetime.datetime.fromisoformat(last_request_time_str)
    current_time = datetime.datetime.now(datetime.timezone.utc)
    time_diff = current_time - last_request_time
    time_diff_seconds = time_diff.total_seconds()
    if time_diff_seconds <= 30:
        with open('nb_request.txt', 'r') as f:
            nb_request = f.read()
        payload={
            "content": None,
            "embeds": [
                {
                    "title": "Statut du bot",
                    "description": f"Le bot est **ONLINE** 🟢\n\n🌐 Sa dernière requête était il y a {time_diff_seconds} secondes. \n\n🚀 Prochaine requête dans {20 - time_diff_seconds} secondes. \n\n 📊 Nombre de requêtes : {nb_request}",
                    "color": 5814783,
                    "footer": {
                        "text": f"{datetime.datetime.now(tz)}"
                    }
                }
            ],
            "attachments": []
                }
        requests.post(url_discord, json=payload)
    else:
        payload={
        "content": None,
            "embeds": [
                {
                    "title": "Statut du bot",
                    "description": f"Le bot est **OFFLINE** 🔴\n\n🌐 Sa dernière requête était {last_request_time}.",
                    "color": 5814783,
                    "footer": {
                        "text": f"{datetime.datetime.now(tz)}"
                    }
                }
            ],
            "attachments": []
                }
        requests.post(url_discord, json=payload)


client.run('TOKEN_HERE')
