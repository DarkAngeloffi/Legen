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

class TicketDropdown(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Support",
                description="Άνοιγμα support ticket",
                emoji="🎫"
            )
        ]

        super().__init__(
            placeholder="Διάλεξε κατηγορία...",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        category = discord.utils.get(
            interaction.guild.categories,
            name="Tickets"
        )

        if category is None:
            category = await interaction.guild.create_category("Tickets")

        channel = await interaction.guild.create_text_channel(
            f"ticket-{interaction.user.name}",
            category=category
        )

        await channel.send(
            f"{interaction.user.mention} Καλώς ήρθες στο ticket σου!"
        )

        await interaction.response.send_message(
            f"Το ticket δημιουργήθηκε: {channel.mention}",
            ephemeral=True
        )

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

@bot.command()
async def ticket(ctx):

    embed = discord.Embed(
        title="Most Wanted® Tickets",
        description="Διάλεξε κατηγορία για να ανοίξεις ticket.",
        color=0x9b59b6
    )

    embed.set_image(
        url="https://imgur.com/a/MmRku1d"
    )

    await ctx.send(
        embed=embed,
        view=TicketView()
    )
    
# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
 keep_alive()
bot.run(TOKEN)


