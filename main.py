import os
import discord
from discord.ext import commands
from discord.ui import Button, View 
from details import extract_details_by_email
from cert_gen import create_certificate
from io import BytesIO
from humanize import number
from dotenv import load_dotenv
from config import total_teams, ctfd_domain, excellence_criteria

load_dotenv()
api_key = os.getenv("DISCORD_API_KEY")
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="?", intents=intents)
user_inputs = {}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return
    
    user_id = message.author.id
    try:
        email, your_name = message.content.split(",", maxsplit=1)
        email = email.strip()
        your_name = your_name.strip()
        try:
            data = await extract_details_by_email(email)
            if data is not None:
                team_name = data['team_name']
                place = data['place']
                excellence = False
                if int(place) < excellence_criteria + 1:
                    excellence = True
                if excellence:
                    image = create_certificate("excellence_template.png", your_name, number.ordinal(int(place)), team_name)
                    with BytesIO() as img:
                        image.save(img, "PNG")
                        img.seek(0)
                        discord_file = discord.File(img, filename='image.png')
                        await message.author.send(f"Congratulations `{your_name}` :tada: You team `{team_name}` got {number.ordinal(int(place))} place out of {total_teams} teams. Great work :clap: :clap:", file=discord_file)
                else:
                    image = create_certificate("participation_template.png", your_name, number.ordinal(int(place)), team_name)
                    with BytesIO() as img:
                        image.save(img, "PNG")
                        img.seek(0)
                        discord_file = discord.File(img, filename='image.png')
                        await message.channel.send(f"Congratulations `{your_name}` :tada: You team `{team_name}` got {number.ordinal(int(place))} place out of {total_teams} teams.", file=discord_file)
            else:
                await message.channel.send(f"The email you provided is not listed on the scoreboard. Please verify the email you provided is associated with [{ctfd_domain}](https://{ctfd_domain})")
        except Exception as e:
            print(e)
            await message.channel.send("Error getting details...")

    except ValueError:
        await message.channel.send("Invalid format. Please provide both email and name on the certificate (format: email, your name on certificate).")
         
bot.run(api_key)
