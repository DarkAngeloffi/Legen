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
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# SETTINGS
# =========================

TICKET_CATEGORY_NAME = "TICKETS"
SUPPORT_ROLE_NAME = "Support"

# Images / Logos
TICKET_BANNER = "https://imgur.com/a/KtJM0O9#1NNw3s3"
TICKET_OPEN_IMAGE = "https://imgur.com/a/KtJM0O9#1NNw3s3"
APPLICATIONS_BANNER = "https://imgur.com/a/KtJM0O9#1NNw3s3"
LOGO_IMAGE = "https://imgur.com/a/KtJM0O9#eynLN19"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="👋 — Welcome to Ticket Support",
            description=(
                "Thank you for contacting our support team. "
                "We've received your ticket and a member of our staff "
                "will assist you as soon as possible."
            ),
            color=0x2b2d31
        )

        embed.add_field(
            name="💯 — Need To Know",
            value="Please stay patient and avoid spamming the ticket.",
            inline=False
        )

        embed.set_image(url=TICKET_OPEN_IMAGE)
        embed.set_thumbnail(url=LOGO_IMAGE)

        close_button = Button(label="Close Ticket", emoji="🔒", style=discord.ButtonStyle.red)

        async def close_callback(interaction2: discord.Interaction):
            await interaction2.channel.delete()

        close_button.callback = close_callback

        view = View(timeout=None)
        view.add_item(close_button)

        await channel.send(
            content=f"{user.mention}",
            embed=embed,
            view=view
        )

        await interaction.response.send_message(
            f"Το ticket σου δημιουργήθηκε: {channel.mention}",
            ephemeral=True
        )


class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


@bot.command()
async def ticket(ctx):
    embed = discord.Embed(
        title="Quantum® Tickets",
        description=(
            "💎 Για να βρεθείτε σε άμεση επικοινωνία με την ομάδα μας, "
            "παρακαλώ δημιουργήστε ticket επιλέγοντας κατηγορία.\n\n"
            "📌 Το support είναι εδώ για να σας βοηθήσει.\n\n"
            "❗ Μπορείτε να έχετε μόνο ένα ticket ενεργό κάθε φορά."
        ),
        color=0x2b2d31
    )

    embed.set_image(url=TICKET_BANNER)
    embed.set_thumbnail(url=LOGO_IMAGE)

    await ctx.send(embed=embed, view=TicketView())

# =========================
# SAY COMMAND
# =========================

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

# =========================
# SAY2 EMBED COMMAND
# =========================

@bot.command()
    await ctx.send(embed=embed)

# =========================
# APPLICATIONS COMMAND
# =========================

bot.command()
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


