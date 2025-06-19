import os
import discord
from discord.ext import commands
from keep_alive import keep_alive  # Import

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.webhooks = True
intents.members = True

# === KONFIGURATION ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
WHITELIST = ['1240934720095653909']

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot ist online als {bot.user.name} ({bot.user.id})')

@bot.event
async def on_webhooks_update(channel):
    try:
        webhooks = await channel.guild.webhooks()
        audit_logs = channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.webhook_create)

        async for entry in audit_logs:
            webhook = next((w for w in webhooks if w.id == entry.target.id), None)
            if webhook:
                executor_id = str(entry.user.id)
                if executor_id not in WHITELIST:
                    await webhook.delete(reason='Nicht autorisierter Webhook-Ersteller')
                    print(f'🛑 Webhook von {executor_id} gelöscht (nicht in Whitelist).')
                else:
                    print(f'✅ Erlaubter Webhook von {executor_id}')
    except Exception as e:
        print(f'⚠️ Fehler beim Webhook-Check: {e}')

keep_alive()  # Startet den Webserver
bot.run(BOT_TOKEN)  # Startet den Bot
