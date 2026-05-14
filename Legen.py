import os
import discord
from flask import Flask
from threading import Thread
from discord.ext import commands

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
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_CATEGORY_NAME = "TICKETS"
STAFF_ROLE_NAME = "Support"


# -----------------------------
# BUTTON VIEW
# -----------------------------
class TicketButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Άνοιγμα Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: Button):

        user = interaction.user
        guild = interaction.guild

        # Έλεγχος αν υπάρχει ήδη ticket
        for channel in guild.channels:
            if channel.name == f"ticket-{user.name.lower()}":
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

        # Δημιουργία channel με το όνομα του χρήστη
        channel = await guild.create_text_channel(
            name=f"ticket-{user.name.lower()}",
            category=category,
            overwrites=overwrites
        )

        # Embed με το όνομα του χρήστη
        embed = discord.Embed(
            title=f"🎫 Ticket από {user.name}",
            description=(
                f"{user.mention}, γράψε εδώ το μήνυμά σου.\n"
                "Μπορείς να ανεβάσεις **όποια εικόνα θέλεις** και να γράψεις **ό,τι θέλεις**."
            ),
            color=0x00aaff
        )

        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)

        await channel.send(f"👋 Καλωσήρθες {user.mention} στο ticket σου!")
        await channel.send(embed=embed)

        await interaction.response.send_message(
            "✅ Το ticket σου δημιουργήθηκε!",
            ephemeral=True
        )


# -----------------------------
# PANEL COMMAND
# -----------------------------
@bot.command()
async def panel(ctx):

    embed = discord.Embed(
        title="🎧 Ticket Support Panel",
        description=(
            "Καλωσήρθες στο σύστημα υποστήριξης!\n\n"
            "📩 Πάτα το κουμπί από κάτω για να ανοίξεις ticket.\n"
            "📸 Μπορείς να βάλεις **όποια εικόνα θέλεις**.\n"
            "📝 Μπορείς να γράψεις **ό,τι κείμενο θέλεις**.\n"
        ),
        color=0xff8800
    )

    # Βάλε εδώ όποια εικόνα θέλεις
    embed.set_thumbnail

# -----------------------------
# RUN BOT
# -----------------------------
if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
