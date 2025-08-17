import discord
import os
import logging
import sys
import asyncio
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Select, Button

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

# Configuration from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1400079467589931018
CHANNEL_ID = 1400179503556329634
ROLE_ID = 1401194121741340693

# Full menu for cash register functionality
menu = {
    "Cheeseburger": 19.99,
    "Deluxe Burger": 24.99,
    "Bacon Burger": 22.99,
    "Mushroom Burger": 27.99,
    "French Fries": 8.99,
    "Onion Rings": 10.99,
    "Soda": 5.99,
    "Milkshake": 9.99
}

class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        try:
            # Try to sync to the specific guild first
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print("✅ Slash commands synced to guild")
        except discord.Forbidden:
            print("⚠️ Cannot sync to guild (insufficient permissions), trying global sync...")
            try:
                # Fallback to global sync if guild sync fails
                await self.tree.sync()
                print("✅ Slash commands synced globally (may take up to 1 hour to appear)")
            except Exception as e:
                print(f"❌ Failed to sync commands: {e}")
        except Exception as e:
            print(f"❌ Error during command sync: {e}")

bot = MyClient()

class OrderView(View):
    def __init__(self):
        super().__init__(timeout=180)
        self.order_items = {}  # Store cart items

        # Dropdown for menu items
        self.item_select = Select(
            placeholder="Select an item",
            options=[discord.SelectOption(label=item, description=f"${price:.2f}") for item, price in menu.items()],
            min_values=1,
            max_values=1
        )

        # Dropdown for quantity
        self.qty_select = Select(
            placeholder="Select quantity",
            options=[discord.SelectOption(label=str(i), value=str(i)) for i in range(1, 11)],
            min_values=1,
            max_values=1
        )

        # Dropdown callbacks
        async def item_callback(interaction: discord.Interaction):
            await interaction.response.defer()

        async def qty_callback(interaction: discord.Interaction):
            await interaction.response.defer()

        self.item_select.callback = item_callback
        self.qty_select.callback = qty_callback

        # Button to add item to cart
        self.add_btn = Button(label="Add to Cart", style=discord.ButtonStyle.blurple)

        # Button to confirm order
        self.confirm_btn = Button(label="Confirm Order", style=discord.ButtonStyle.green)

        # Callbacks
        async def add_callback(interaction: discord.Interaction):
            if not self.item_select.values or not self.qty_select.values:
                await interaction.response.send_message("❌ Please select both item and quantity first.", ephemeral=True)
                return
                
            item = self.item_select.values[0]
            qty = int(self.qty_select.values[0])
            self.order_items[item] = self.order_items.get(item, 0) + qty
            await interaction.response.send_message(f"✅ Added {item} x{qty} to cart.", ephemeral=True)

        async def confirm_callback(interaction: discord.Interaction):
            if not self.order_items:
                await interaction.response.send_message("❌ Cart is empty.", ephemeral=True)
                return

            total = 0
            receipt = "🧾 **Marble Burger House Receipt**\n----------------------------\n"
            for item, qty in self.order_items.items():
                price = menu[item] * qty
                total += price
                receipt += f"{item} x{qty} - ${price:.2f}\n"

            receipt += "----------------------------\n"
            receipt += f"**Total: ${total:.2f}**"
            await interaction.response.send_message(receipt)

        self.add_btn.callback = add_callback
        self.confirm_btn.callback = confirm_callback

        # Add all UI elements
        self.add_item(self.item_select)
        self.add_item(self.qty_select)
        self.add_item(self.add_btn)
        self.add_item(self.confirm_btn)

@bot.tree.command(name="deployment", description="Create a deployment announcement", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(
    host="Who is hosting the deployment?",
    cohost="Who is co-hosting?",
    when="When is the deployment?",
    promotional="Is this promotional? (yes/no)"
)
async def deployment(interaction: discord.Interaction, host: str, cohost: str, when: str, promotional: str):
    promo_status = "✅ Yes" if promotional.lower() in ["yes", "y", "true", "promo"] else "❌ No"

    embed = discord.Embed(
        title="🚨 Deployment Announcement",
        description="A deployment is being hosted. Please react if you're attending!",
        color=discord.Color.red()
    )
    embed.add_field(name="👑 Host", value=host, inline=True)
    embed.add_field(name="🤝 Co-Host", value=cohost, inline=True)
    embed.add_field(name="📅 When", value=when, inline=True)
    embed.add_field(name="🎁 Promotional?", value=promo_status, inline=True)
    embed.set_footer(text="Deployment Bot • Thank you for your service")

    channel = bot.get_channel(CHANNEL_ID)
    role_mention = f"<@&{ROLE_ID}>"

    if channel:
        sent_message = await channel.send(role_mention, embed=embed)
        await sent_message.add_reaction("✅")
        await interaction.response.send_message("✅ Deployment embed sent successfully.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Could not find the channel.", ephemeral=True)

@bot.tree.command(name="order", description="Place an order from the menu", guild=discord.Object(id=GUILD_ID))
async def order(interaction: discord.Interaction):
    # Role check
    if not any(role.id == ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return

    await interaction.response.send_message("📝 Build your order below:", view=OrderView(), ephemeral=True)

@bot.event
async def on_ready():
    logger.info(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    
    # Start heartbeat task
    asyncio.create_task(heartbeat_task())

@bot.event
async def on_disconnect():
    logger.warning("⚠️ Bot disconnected from Discord")

@bot.event
async def on_resumed():
    logger.info("🔄 Bot reconnected to Discord")

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f"❌ Bot error in {event}: {args}")

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"❌ Command error: {error}")

async def heartbeat_task():
    """Periodic heartbeat to ensure bot stays responsive"""
    while True:
        try:
            await asyncio.sleep(300)  # 5 minutes
            if bot.is_ready():
                logger.info("💓 Bot heartbeat - all systems operational")
            else:
                logger.warning("💔 Bot heartbeat - not ready, may need restart")
        except Exception as e:
            logger.error(f"❌ Heartbeat error: {e}")

# Enhanced startup with better error handling
async def run_bot_async():
    """Run bot with enhanced error handling"""
    try:
        await bot.start(DISCORD_TOKEN, reconnect=True)
    except discord.LoginFailure:
        logger.error("❌ Invalid Discord token")
        raise
    except discord.ConnectionClosed:
        logger.warning("⚠️ Connection closed, attempting restart...")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected bot error: {e}")
        raise

if DISCORD_TOKEN:
    try:
        asyncio.run(run_bot_async())
    except KeyboardInterrupt:
        logger.info("👋 Bot shutdown requested")
    except Exception as e:
        logger.error(f"❌ Bot failed to start: {e}")
        raise
else:
    logger.error("❌ No Discord token found. Please set DISCORD_TOKEN environment variable.")
    raise ValueError("Missing Discord token")