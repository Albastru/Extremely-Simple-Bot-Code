# IMPORT FUNCTIONS

from bot_token import token #   Bot Token would be a local file containing the token for your applications bot; "token" is a constant. For example, your file might read «token = "abcd1234"»
import discord as db    #   "discord" is an installed API, and is imported as "db" for simplicity when called. DB in this case stands for "discord bot", but you can import it under any name you'd like.
import discord.ext
import json


client = db.Client()

warnedPeople = {}   #   This would be a list of the users in your server that have been warned.
badWords =("One", "Two", "Three", "Four")   #   This is a list of bad words which your bot will look out for.

@client.event
async def on_ready():   #   When the bot runs,
    print("Bot is ready and running!")  #   this is printed in the terminal. It shows things have started correctly.
    activity = db.Activity(type=db.ActivityType.listening, name="to your commands!")    #   Discord allows for "playing" or "listening" statuses. The bot would display "listening to your commands!" as its status.
    await client.change_presence(activity=activity) #   Sets the bot activity as to that defined above.

@client.event
async def on_message(message):  #   When a message is sent...

    #   A psuedo-mute command, so that things are kept simple for now.
    try:
        if len(warnedPeople[message.author.id]) >= 2:   #   If warnings >/ 2,
            await message.channel.purge(limit=1)    #   delete the message from the warned user
            return
            #   This stops users with two or more warnings from sending a message.
    except KeyError:
        warnedPeople[message.author.id] = []

    if message.content.startswith("!hello"):    #   When a server member sends "!hello",
        await message.channel.send("Hello, user!")  #   we want to send a pleasant greeting. This does not mention the user so that it is kept simple. 

    if any(word in message.content for word in badWords):   #   If a message is found to contain a word from the "badWords" list,
        await warn_user(author=message.author.id, message=message.content)  #   warn the user;
        await message.channel.purge(limit=1)    #   delete the message with the bad word;
        await message.channel.send("Please don't use those words here!")    #   Notify the user that they've sent a banned word.

    elif message.content.startswith("!delete"): #   If the message contains "!delete",
        how_many = int(message.content.split("!delete ", 1)[1]) # Select the quantity of messages to delete by splitting n from "!delete". E.g. "!delete 5" becomes "!delete" & "5", where  is taken as "how_many"
        await message.channel.purge(limit=how_many + 1) #   delete the message. Note that this command will delete two messages: n messages AND the command message.

    elif message.content.startswith("!developer"):  #   If the message contains "!developer",
        embed = discord.Embed(title="Developed by [Y/N]", description="[Find me here!](https://www.example.com/)", color=389978)    # create a discord embed. Add a title, a descriptor with a link embedded, and a colour.
        embed.set_image(url="https://cdn.fellowsfilm.com/avatars/o/9/9905.jpg?1611921237") #    Add an image to the embed.
        await message.channel.send(embed=embed) #   Send the response to the command, with the embed set to that defined above.

# Commands list & help

    elif message.content.startswith("!commands"):   #   If the message contains "!commands",
        embed = discord.Embed(title="Commands list", description="[Use 'c!{command} for a description]", color=389978)  #   create an embed with a title, a descriptor, and a colour.
        embed.set_image(url="www.example.com/image.png")    #   Add an image to the embed.
        await message.channel.send(embed=embed) #   Send the response to the command, with the embed set to that defined above.
   
    elif message.content.startswith("c!hello"):   #   If the message contains "c!hello",
        embed = discord.Embed(title="How to use the !hello command", description="Use !hello when you feel lonely - the bot will greet you!", color=389978)  #   create an embed with a title, a descriptor, and a colour.
        await message.channel.send(embed=embed) #   Send the response to the command, with the embed set to that defined above.

    elif message.content.startswith("c!delete"):   #   If the message contains "c!delete",
        embed = discord.Embed(title="How to use the !delete command", description="Use !delete to delete messaages in the chat. Enter !delete + no. of messages!", color=389978)  #   create an embed with a title, a descriptor, and a colour.
        await message.channel.send(embed=embed) #   Send the response to the command, with the embed set to that defined above.

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
