#Google Calendar API imports
from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import json
import os
import discord
import requests
from discord.ext import commands
import random
from keepalive import keepalive

# enter token for the server
TOKEN = os.environ['DISCORD_TOKEN']

# client = commands.Bot(command_prefix='.')

import discord
from discord.ext import commands
# from dotenv import load_dotenv
# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# ---------------------BOT COMMAND
bot = commands.Bot(command_prefix='!')
# ---------------------WEB SCRAPING
scraping = open("ok.json", encoding="UTF-8")
scraped = json.load(scraping)
# ----------------FOR HELPLINE
helplines = ["Family Violence Prevention Center 1-800-313-1310",
             "National Sexual Assault Hotline 1-800-656-HOPE (4673)",
             "Drug Abuse National Helpline 1-800-662-4357",
             "American Cancer Society 1-800-227-2345",
             "Eating Disorders Awareness and Prevention 1-800-931-2237",
             "GriefShare 1-800-395-5755",
             "Suicide Hotline 1-800-SUICIDE (784-2433)"]

@bot.command(aliases=['event', 'nextevent', 'nextevents', 'upcomingevent', 'upcomingevents'], help='Get a list of the ongoing and upcoming events of the pod')
async def events(ctx, count='1'):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Code to get the calendar id 

    # page_token = None
    # while True:
    #     calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #     for calendar_list_entry in calendar_list['items']:
    #         print(calendar_list_entry)
    #     page_token = calendar_list.get('nextPageToken')
    #     if not page_token:
    #         break    

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming', int(count), 'events')
    events_result = service.events().list(calendarId='6hkc92l58daaolq2h0meri3m0g@group.calendar.google.com', timeMin=now,
                                        maxResults=int(count), singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        await ctx.send('No upcoming events found.')
    else:
        a = "Here's the list of upcoming/ongoing " + count + " event(s)"
        await ctx.send(a)
        for no, event in enumerate(events):
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            # print(start, event['summary'], event['location'], event['description'])
            b = str(no+1) + ' - ' + event['summary']
            await ctx.send(b)
            c = 'Starts at: ' + start
            await ctx.send(c)
            d = 'Ends at: ' + end
            await ctx.send(d)
            e = 'Location: ' + event['location']
            await ctx.send(e)
            # await ctx.send(event['description'])


@bot.command(name='faq', help='Searches the FAQ for the most relevant section corresponding to the provided keyword.')
async def faq(ctx, keyword):
    for i in scraped["intents"]:
        if(keyword==i["tag"]):
            quote = i["responses"]
    # response = quote
    for i in quote:
        response = i
        await ctx.send(response)


@bot.command(aliases=['al'])
async def all(ctx):
    for i in helplines:
        res = i
        await ctx.send(res)

@bot.command(aliases=['depression'])
async def suicide(ctx):
    await ctx.send(helplines[6])

@bot.command(aliases=['violenT'])
async def violence(ctx):
    await ctx.send(helplines[0])

@bot.command(aliases=['drugs'])
async def drugabuse(ctx):
    await ctx.send(helplines[2])

@bot.command(aliases=['assault'])
async def sexualAssault(ctx):
    await ctx.send(helplines[1])

@bot.command(aliases=['ILLNESS'])
async def cancer(ctx):
    await ctx.send(helplines[3])

@bot.command(aliases=['grie'])
async def grief(ctx):
    await ctx.send(helplines[5])

@bot.command(aliases=['eating'])
async def eatingdisorder(ctx):
    await ctx.send(helplines[4])

# -------------------------MENTAL WELL BEING BOT
greetings = ["hi", "hello","how are you", "whats up","hey"]
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "stressed", "hopeless", "unhappy","worthless"]
problems = ["time management", "busy", "impostor", "coding"]
suicide = ["kill myself", "kill yourself","suicidal","death"]

# ------------replies
greet = [
    "Welcome !. What can I do for you?",
    "Hi!!",
    "I am so excited to have you here!",
    "Hello there, I am an MLH bot here for your help",
    "No I am sleeping right now. Just kidding !! how may I help you?"
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

# -------------------------TRIGGERING BOT EVENT
@bot.event
async def on_ready():
    print('Bot is ready.')
#-------------------------RANDOM QUOTE SUGGESTION
def get_qoute():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)
# ------------------------GET RANDOM JOKES
def joke():
    url = "https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Christmas?blacklistFlags=nsfw,political,racist,sexist,explicit&type=twopart"
    response = requests.get(url)
    json_data = json.loads(response.text)
    jokes = ""
    jokes = json_data["setup"] + "  -  " + json_data["delivery"]
    return(jokes)

# -----------------------MAIN BOT CHAT EVENT
@bot.event
async def on_message(message):
    flag = False
    gify = False
    await bot.process_commands(message)
    msg = message.content
    if message.author == bot.user:
        return
    if any(word in msg for word in greetings):
        gify = True
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

    if 'quote' in msg.lower():
        response = get_qoute()
        await message.channel.send(response)

# REPEATEDLY PING SERVER TO KEEP ALIVE
#keepalive()

# ---------------------INITIALIZING THE BOT
bot.run(TOKEN)
