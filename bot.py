import discord
from discord import app_commands
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os
from datetime import datetime
from models import add_response_to_notion

load_dotenv(override=True)

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

print(f"Using Channel ID: {CHANNEL_ID}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    print(f'Bot intents: {bot.intents}')
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    await bot.wait_until_ready()

# Admin slash commands
@bot.tree.command(name="start", description="Start daily updates (Admin only)")
@app_commands.default_permissions(administrator=True)
async def start(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need administrator permissions.", ephemeral=True)
        return
    
    send_daily_message.start()
    await interaction.response.send_message("Daily updates started!", ephemeral=True)

@bot.tree.command(name="stop", description="Stop daily updates (Admin only)")
@app_commands.default_permissions(administrator=True)
async def stop(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need administrator permissions.", ephemeral=True)
        return
    
    send_daily_message.cancel()
    await interaction.response.send_message("Daily updates stopped!", ephemeral=True)

@bot.tree.command(name="status", description="Check bot status (Admin only)")
@app_commands.default_permissions(administrator=True)
async def status(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need administrator permissions.", ephemeral=True)
        return
    
    is_running = send_daily_message.is_running()
    status_msg = "Bot is currently sending daily updates" if is_running else "Bot is not sending daily updates"
    await interaction.response.send_message(status_msg, ephemeral=True)

@tasks.loop(hours=24)
async def send_daily_message():
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Channel with ID {CHANNEL_ID} not found.")
            return

        # Get channel-specific members
        channel_members = channel.members
        print(f"Total channel members: {len(channel_members)}")
        
        members = []
        for member in channel_members:
            if member.bot:
                print(f"Skipping bot: {member.name}")
                continue
            
            permissions = channel.permissions_for(member)
            if not permissions.read_messages:
                print(f"Skipping member {member.name} - no read permissions")
                continue
                
            members.append(member)
            print(f"Added channel member: {member.name}")

        if not members:
            print(f"No valid members found in channel {CHANNEL_ID}")
            return

        print(f"Sending messages to {len(members)} members")
        
        for member in members:
            try:
                dm_channel = await member.create_dm()
                await dm_channel.send("Please respond with your daily update.")
                print(f"Message sent to {member.name}")
            except discord.Forbidden:
                print(f"Cannot DM {member.name} - DMs closed")
            except Exception as e:
                print(f"Error messaging {member.name}: {e}")
                
    except Exception as e:
        print(f"Error in send_daily_message: {e}")

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and not message.author.bot:
        try:
            user = message.author.name
            response = message.content
            
            add_response_to_notion(user, response)
            
            await message.channel.send("Response recorded, thank you!")
            print(f"Recorded response from {user}")
            
        except Exception as e:
            print(f"Error processing response from {message.author.name}: {e}")
            await message.channel.send("Error processing your response.")

    await bot.process_commands(message)

bot.run(DISCORD_BOT_TOKEN)