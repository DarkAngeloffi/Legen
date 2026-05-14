import discord
import flask
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

# -----------------------------
# ΡΥΘΜΙΣΕΙΣ
# -----------------------------
TICKET_CATEGORY_NAME = "TICKETS"   # Η κατηγορία όπου θα ανοίγουν τα tickets
STAFF_ROLE_NAME = "Support"        # Ρόλος που θα βλέπει τα tickets

# -----------------------------
# ΕΛΕΓΧΟΣ ΑΝ Ο ΧΡΗΣΤΗΣ ΕΧΕΙ ΗΔΗ TICKET
# -----------------------------
def user_has_ticket(guild, user):
    for channel in guild.channels:
        if channel.name == f"ticket-{user.id}":
            return True
    return False

# -----------------------------
# ΔΗΜΙΟΥΡΓΙΑ TICKET
# -----------------------------
@bot.command()
async def ticket(ctx):
    user = ctx.author
    guild = ctx.guild

    # Έλεγχος αν έχει ήδη ticket
    if user_has_ticket(guild, user):
        await ctx.send("❗ Έχεις ήδη ανοιχτό ticket.")
        return

    # Βρίσκουμε/δημιουργούμε την κατηγορία
    category = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
    if category is None:
        category = await guild.create_category(TICKET_CATEGORY_NAME)

    # Βρίσκουμε το staff role
    staff_role = discord.utils.get(guild.roles, name=STAFF_ROLE_NAME)

    # Δημιουργία private channel
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

    # Μήνυμα μέσα στο ticket
    embed = discord.Embed(
        title="🎫 Ticket Created",
        description="Γράψε εδώ το μήνυμα που θέλεις.\nΜπορείς να ανεβάσεις **όποια εικόνα θέλεις**.",
        color=0x00aaff
    )

    await channel.send(f"{user.mention} καλωσήρθες στο ticket σου!")
    await channel.send(embed=embed)

    await ctx.send("✅ Το ticket σου δημιουργήθηκε!")

# -----------------------------
# ΚΛΕΙΣΙΜΟ TICKET
# -----------------------------
@bot.command()
async def close(ctx):
    if "ticket-" not in ctx.channel.name:
        await ctx.send("❗ Αυτή η εντολή χρησιμοποιείται μόνο μέσα σε ticket.")
        return

    await ctx.send("🔒 Το ticket θα κλείσει σε 3 δευτερόλεπτα...")
    await ctx.channel.delete()
# -----------------------------
# RUN BOT
# -----------------------------
if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
