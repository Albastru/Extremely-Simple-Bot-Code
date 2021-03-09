# IMPORT FUNCTIONS

from bot_token import token
import discord as db
import discord.ext
import json


client = db.Client()

warnedPeople = {}
badWords =("One", "Two", "Three", "Four")

@client.event
async def on_ready():
    print("Bot is ready and running!")
    activity = db.Activity(type=db.ActivityType.listening, name="to your commands!")
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):

# Generic Commands Below

    try:
        if len(warnedPeople[message.author.id]) >= 2:
            await message.channel.purge(limit=1)
            return
    except KeyError:
        warnedPeople[message.author.id] = []

    if message.content.startswith("!hello"):
        await message.channel.send("Hello, user!")

    if any(word in message.content for word in badWords):
        await warn_user(author=message.author.id, message=message.content)
        await message.channel.purge(limit=1)
        await message.channel.send("Please don't use those words here!")

    elif message.content.startswith("!delete"):
        how_many = int(message.content.split("!delete ", 1)[1])
        await message.channel.purge(limit=how_many + 1)

    elif message.content.startswith("!developer"):
        embed = discord.Embed(title="Developed by Albastru", description="[Find me here!](https://fellowsfilm.com/members/ecronbuses.9905/)", color=389978)
        embed.set_image(url="https://cdn.fellowsfilm.com/avatars/o/9/9905.jpg?1611921237")
        await message.channel.send(embed=embed)

# Commands list & help

    elif message.content.startswith("!commands"):
        embed = discord.Embed(title="Commands list", description="[Use 'c!{command} for a description]", color=389978)
        embed.set_image(url="https://media.discordapp.net/attachments/808121412044849152/818894259607699506/TGA.png")
        await message.channel.send(embed=embed)

    elif message.content.startswith("c!hello"):
        embed = discord.Embed(title="How to use the !hello command", description="Use !hello when you feel lonely - the bot will greet you!", color=389978)
        await message.channel.send(embed=embed)

    elif message.content.startswith("c!delete"):
        embed = discord.Embed(title="How to use the !delete command", description="Use !delete to delete messaages in the chat. Enter !delete + no. of messages!", color=389978)
        await message.channel.send(embed=embed)

# Warn system Below

async def warn_user(author, message):
    global warnedPeople
    if author in warnedPeople.keys():
        warnedPeople[author].append(message)
    else:
        warnedPeople[author] = [message]
    with open("userdata.json", mode="w") as file:
        json.dump(warnedPeople, file)

client.run(token)