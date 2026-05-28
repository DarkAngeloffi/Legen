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


# -----------------------------
# SELECT MENU VIEW
# -----------------------------
class TicketSelect(View):
    def __init__(self):
        super().__init__(timeout=None)

        options = [
            discord.SelectOption(label="Support", description="Άνοιγμα ticket για υποστήριξη", emoji="🛠️"),
            discord.SelectOption(label="Report", description="Αναφορά χρήστη ή προβλήματος", emoji="⚠️"),
            discord.SelectOption(label="Appeal", description="Αίτηση unban/unmute", emoji="📨"),
        ]

        self.add_item(
            Select(
                placeholder="Επίλεξε κατηγορία ticket...",
                min_values=1,
                max_values=1,
                options=options,
                custom_id="ticket_select"
            )
        )

    @discord.ui.select(custom_id="ticket_select")
    async def select_callback(self, interaction: discord.Interaction, select: Select):

        user = interaction.user
        guild = interaction.guild
        choice = select.values[0]

        # Έλεγχος αν υπάρχει ήδη ticket
        for channel in guild.channels:
            if channel.name == f"ticket-{user.id}":
                await interaction.response.send_message(
                    "❗ Έχεις ήδη ανοιχτό ticket.",
                    ephemeral=True
                )
                return

        # Βρίσκουμε/δημιουργούμε κατηγορία
        category = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(TICKET_CATEGORY_NAME)

        staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await guild.create_text_channel(
            name=f"ticket-{user.id}",
            category=category,
            overwrites=overwrites
        )

        await channel.send(f"{user.mention} άνοιξες ticket για **{choice}**.\nΓράψε το μήνυμά σου εδώ.")

        await interaction.response.send_message(
            f"✅ Το ticket σου δημιουργήθηκε στην κατηγορία **{choice}**!",
            ephemeral=True
        )


# -----------------------------
# PANEL COMMAND
# -----------------------------
@bot.command()
async def panel(ctx):
    await ctx.send(
        "🎫 **Ticket Panel**\nΕπίλεξε από το menu για να ανοίξεις ticket.",
        view=TicketSelect()
    )


# -----------------------------
# CLOSE COMMAND
# -----------------------------
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


