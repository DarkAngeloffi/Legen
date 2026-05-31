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

TICKET_CATEGORY_NAME = "TICKETS"
STAFF_ROLE_NAME = "Support"

# ---------------------------------------------------
# CONFIG — Εσύ αλλάζεις ό,τι θέλεις εδώ
# ---------------------------------------------------

BANNER_URL = "https://imgur.com/a/MmRku1d"   # Βάλε όποιο banner θες
PANEL_TEXT = """
Welcome to Summer Test Roleplay

Για την άμεση εξυπηρέτηση σας μπορείτε να ανοίξετε ένα ticket ώστε να μιλήσετε με κάποιον ανώτερο και να λύσετε το πρόβλημα σας.
"""

CATEGORIES = [
    ("Support", "Υποστήριξη για προβλήματα", "🛠️"),
    ("Report", "Αναφορά χρήστη ή προβλήματος", "⚠️"),
    ("Appeal", "Αίτηση unban/unmute", "📨"),
]
# ---------------------------------------------------


class TicketPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

        options = [
            discord.SelectOption(
                label=name,
                description=desc,
                emoji=emoji
            )
            for name, desc, emoji in CATEGORIES
        ]

        self.select = Select(
            placeholder="Choose a category",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_select"
        )

        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        choice = self.select.values[0]

        # Έλεγχος αν υπάρχει ήδη ticket
        for channel in guild.channels:
            if channel.name == f"ticket-{user.id}":
                await interaction.response.send_message(
                    "❗ Έχεις ήδη ανοιχτό ticket.",
                    ephemeral=True
                )
                return

        # Δημιουργία κατηγορίας αν δεν υπάρχει
        category = discord.utils.get(guild.categories, name="TICKETS")
        if category is None:
            category = await guild.create_category("TICKETS")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category,
            overwrites=overwrites
        )

        await channel.send(f"{user.mention} άνοιξες ticket για **{choice}**.")

        await interaction.response.send_message(
            f"✅ Το ticket σου δημιουργήθηκε στην κατηγορία **{choice}**!",
            ephemeral=True
        )


@bot.command()
async def panel(ctx):
    # Στέλνουμε την εικόνα σαν attachment
    await ctx.send(BANNER_URL)

    # Στέλνουμε το κείμενο + container
    await ctx.send(PANEL_TEXT, view=TicketPanel())


@bot.command()
async def close(ctx):
    if "ticket-" not in ctx.channel.name:
        await ctx.send("❗ Αυτή η εντολή χρησιμοποιείται μόνο μέσα σε ticket.")
        return

    await ctx.send("🔒 Το ticket θα κλείσει σε 3 δευτερόλεπτα...")
    await ctx.channel.delete()

# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
 keep_alive()
bot.run(TOKEN)


