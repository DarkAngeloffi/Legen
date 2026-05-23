import os
import discord
from flask import Flask
from threading import Thread
from discord.ext import commands
from discord.ui import View, Select, Button

app = Flask('')

@app.route('/')
def home():
    return "OK"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
# =========================
# APPLICATIONS COMMAND
# =========================

@bot.command()
async def applications(ctx):
    embed = discord.Embed(
        title="💎 Κάνε μια αίτηση σήμερα!",
        description=(
            "Βοήθησε ως Staff ή εξέλιξε το roleplay σου.\n\n"
            "👮 ΕΛ.ΑΣ → [Αίτηση](https://google.com)\n"
            "🚑 Ε.Κ.Α.Β → [Αίτηση](https://google.com)\n"
            "⚖️ Δικαστικό Μέγαρο → [Αίτηση](https://google.com)\n"
            "💎 Legion Roleplay Staff → [Αίτηση](https://google.com)"
        ),
        color=0x2b2d31
    )

    embed.set_image(url=APPLICATIONS_BANNER)
    embed.set_thumbnail(url=LOGO_IMAGE)

    await ctx.send(embed=embed)

# =========================
# HELP COMMAND
# =========================

bot.remove_command("help")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📖 Help Commands",
        color=0xff00ff
    )

    embed.add_field(
        name="!ticket",
        value="Στέλνει το ticket panel",
        inline=False
    )

    embed.add_field(
        name="!say <message>",
        value="Στέλνει απλό μήνυμα",
        inline=False
    )

    embed.add_field(
        name="!say2 <message>",
        value="Στέλνει embed μήνυμα",
        inline=False
    )

    embed.add_field(
        name="!applications",
        value="Στέλνει applications panel",
        inline=False
    )

    embed.set_thumbnail(url=LOGO_IMAGE)

    await ctx.send(embed=embed)

# =========================
# HELP COMMAND
# =========================

bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📖 Help Commands",
        color=0xff00ff
    )

    embed.add_field(
        name="!ticket",
        value="Στέλνει το ticket panel",
        inline=False
    )

    embed.add_field(
        name="!say <message>",
        value="Στέλνει απλό μήνυμα",
        inline=False
    )

    embed.add_field(
        name="!say2 <message>",
        value="Στέλνει embed μήνυμα",
        inline=False
    )

    embed.add_field(
        name="!applications",
        value="Στέλνει applications panel",
        inline=False
    )

    embed.set_thumbnail(url=LOGO_IMAGE)

    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for v in [TicketView()]:
     bot.add_view(v)
     await bot.change_presence(activity=discord.Game(name="Toxic Reborn Roleplay"))
    print("Bot fully online!")
    
# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
 keep_alive()
bot.run(TOKEN)


