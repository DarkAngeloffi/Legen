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

# ---------- CLOSE BUTTON ----------

class CloseButton(Button):
    def __init__(self):
        super().__init__(
            label="Close Ticket",
            emoji="🔒",
            style=discord.ButtonStyle.danger
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Το ticket κλείνει σε 3 δευτερόλεπτα...",
            ephemeral=True
        )

        await interaction.channel.delete()


# ---------- TICKET VIEW ----------

class TicketControls(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseButton())


# ---------- DROPDOWN ----------

class TicketDropdown(Select):
    def __init__(self):

        options = [
            discord.SelectOption(
                label="Support",
                emoji="🎫",
                description="Άνοιγμα support ticket"
            ),
            discord.SelectOption(
                label="Report",
                emoji="⚠️",
                description="Report χρήστη"
            ),
            discord.SelectOption(
                label="Donation",
                emoji="💎",
                description="Donation support"
            )
        ]

        super().__init__(
            placeholder="Choose a category...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        ticket_name = f"ticket-{user.name.lower()}"

        existing = discord.utils.get(
            guild.channels,
            name=ticket_name
        )

        if existing:
            await interaction.response.send_message(
                f"Έχεις ήδη ticket: {existing.mention}",
                ephemeral=True
            )
            return

        category = discord.utils.get(
            guild.categories,
            name="TICKETS"
        )

        if category is None:
            category = await guild.create_category(
                "TICKETS"
            )

        overwrites = {
            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            user:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )
        }

        channel = await guild.create_text_channel(
            ticket_name,
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="👋 Welcome To Ticket Support",
            description=(
                "Το ticket σου δημιουργήθηκε.\n\n"
                "Περίγραψε το πρόβλημα σου "
                "και ένα μέλος του staff "
                "θα σε εξυπηρετήσει σύντομα."
            ),
            color=0x2b2d31
        )

        await channel.send(
            content=user.mention,
            embed=embed,
            view=TicketControls()
        )

        await interaction.response.send_message(
            f"Το ticket δημιουργήθηκε: {channel.mention}",
            ephemeral=True
        )


class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())


# ---------- COMMAND ----------

@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):

    embed = discord.Embed(
        title="🌊 Welcome To Summer Melody Roleplay",
        description=(
            "Για να επικοινωνήσεις με το staff,\n"
            "επέλεξε κατηγορία από το dropdown."
        ),
        color=0x2b2d31
    )

    # ΒΑΛΕ ΤΗ ΔΙΚΗ ΣΟΥ ΕΙΚΟΝΑ
    embed.set_image(
        url="https://YOUR-BANNER-LINK.png"
    )

    await ctx.send(
        embed=embed,
        view=TicketView()
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    
# =========================
# RUN BOT
# =========================

if __name__ == "__main__":
 keep_alive()
bot.run(TOKEN)


