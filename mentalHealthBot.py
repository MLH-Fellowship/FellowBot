# # bot.py
import json
import os
import discord
import requests
from discord.ext import commands
import random

# enter token for the server
TOKEN = ''
# enter application id
GUILD = ''
flag = False
client = commands.Bot(command_prefix='.')

# -------------keyword corpus
greetings = ["hi", "hello","how are you", "whats up","hey"]
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "stressed", "hopeless", "unhappy","worthless"]
problems = ["time management", "busy", "impostor", "coding"]
suicide = ["kill myself", "kill yourself","suicidal","death"]

# ------------replies
greet = [
    "What can I do for you?",
    "Hi",
    "Hello there, I am an MLH bot here for your help",
    "No I am sleeping right now. Just kidding how may I help you?"
]

starter_encouragements = [
    "At times you may feel like this and I understand that, but it won't be for long I can assure you",
    "Trying going for a walk and disconnecting with your surroundings and listen to music. The best way to cope up is to take a break",
    "I hear you, MLH is there for you. Please talk to your pod leader and tell him in detail what problems are you facing in, he/she will be dhtere for you like we all are",
    "You are doing great. If it counts, I am proud of you ! Don't feel like you cannot do better, you ofcourse can!"
]

copeup=[
    "I can understand totally. But do you know how can you cope up?. Let me help you : 1. Divide your time into blocks"
    "and make sure you are being generous to yourself."
    "2. Make sure you drink enough water and go out for a walk when your mind gets cluttered."
    "3. A little music does not hurt anyone."
    "4. We as coders feel as impostors all the time, don't worry just make sure you have faith on yourself",
    "I can totally understand, have you ever tried the pomodore technique.? Read about it here - https://en.wikipedia.org/wiki/Pomodoro_Technique#:~:text=The%20Pomodoro%20Technique%20is%20a%20time%20management%20method,25%20minutes%20in%20length%2C%20separated%20by%20short%20breaks. "
]

positivereply = [
    "We are extremely sorry to hear that you feel like this , but you are not alone in this. We as MLH put your well being as the top priority. Come talk to us what is bothering you. Help is available, speak with a counselor today by calling the National Suicide Prevention Lifeline at 800-273-8255",
    "WE ARE THERE FOR YOU!!. When you think life isn't worth it, search for some new options. Help is available, speak with a counselor today by calling the National Suicide Prevention Lifeline at 800-273-8255"
]
@client.event
async def on_ready():
    print('Bot is ready.')

def get_qoute():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def joke():
    url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Christmas?blacklistFlags=nsfw,political,racist,sexist,explicit&type=twopart"
    response = requests.get(url)
    json_data = json.loads(response.text)
    jokes = ""
    jokes = json_data["setup"] + "  -  " + json_data["delivery"]
    return(jokes)


@client.event
async def on_message(message):
    flag = False
    await client.process_commands(message)
    msg = message.content
    if message.author == client.user:
        return
    if any(word in msg for word in greetings):
        # flag = True
        response = random.choice(greet)
        await message.channel.send(response)

    if any(word in msg for word in sad_words):
        flag = True
        response = random.choice(starter_encouragements)
        await message.channel.send(response)

    if any(word in msg for word in problems):
        flag = True
        response = random.choice(copeup)
        await message.channel.send(response)

    if any(word in msg for word in suicide):
        flag = True
        response = random.choice(positivereply)
        await message.channel.send(response)

    if(flag):
        r1 = "And just to brighten your day, here is a joke for you"
        await message.channel.send(r1)
        r2 = joke()
        await message.channel.send(r2)

    if 'quote' in message.content.lower():
        response = get_qoute()
        await message.channel.send(response)

client.run(TOKEN)
