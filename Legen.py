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

# Βάλε το banner σου εδώ
BANNER_URL = "https://imgur.com/a/1ZVby8N"

# ---------------- CLOSE BUTTON ----------------

class CloseTicket(Button):
    def __init__(self):
        super().__init__(
            label="Close Ticket",
            emoji="🔒",
            style=discord.ButtonStyle.danger
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.send_message(
            "🔒 This ticket will be closed in 5 seconds..."
        )

        await asyncio.sleep(5)

        await interaction.channel.delete()


# ---------------- TICKET VIEW ----------------

class TicketButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseTicket())


# ---------------- DROPDOWN ----------------

class TicketDropdown(Select):
    def __init__(self):

        options = [

            discord.SelectOption(
                label="Support",
                emoji="🎫",
                description="General support"
            ),

            discord.SelectOption(
                label="Report Player",
                emoji="🚨",
                description="Report a player"
            ),

            discord.SelectOption(
                label="Donation Support",
                emoji="💎",
                description="Donation issues"
            ),

            discord.SelectOption(
                label="Bug Report",
                emoji="🐞",
                description="Report a bug"
            ),

            discord.SelectOption(
                label="Other",
                emoji="❓",
                description="Other requests"
            )

        ]

        super().__init__(
            placeholder="Choose a category",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        user = interaction.user

        prefixes = {
            "Support": "support",
            "Report Player": "report",
            "Donation Support": "donation",
            "Bug Report": "bug",
            "Other": "other"
        }

        ticket_name = f"{prefixes[self.values[0]]}-{user.name.lower()}"

        existing = discord.utils.get(
            guild.text_channels,
            name=ticket_name
        )

        if existing:
            await interaction.response.send_message(
                f"❌ You already have an open ticket: {existing.mention}",
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
            title="🎫 Ticket Support",
            description=(
                f"**Category:** {self.values[0]}\n\n"
                "Please describe your issue.\n"
                "A staff member will help you shortly."
            ),
            color=0x2b2d31
        )

        embed.set_image(url=BANNER_URL)

        await channel.send(
            content=user.mention,
            embed=embed,
            view=TicketButtons()
        )

        await interaction.response.send_message(
            f"✅ Ticket created: {channel.mention}",
            ephemeral=True
        )


class TicketPanel(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())


# ---------------- COMMAND ----------------

@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):

    embed = discord.Embed(
        title="Welcome to 420 Roleplay",
        description=(
            "Για την άμεση εξυπηρέτηση σας μπορείτε να "
            "ανοίξετε ένα ticket ώστε να μιλήσετε με "
            "κάποιον ανώτερο και να λύσετε το πρόβλημα σας."
        ),
        color=0x2b2d31
    )

    # Banner πάνω από το κείμενο
    embed.set_image(url=BANNER_URL)

    await ctx.send(
        embed=embed,
        view=TicketPanel()
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


