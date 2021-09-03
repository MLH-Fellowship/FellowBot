#Google Calendar API imports
#!/usr/bin/env python3
from motivation import get_motivation, refresh_reddit_token
from connect_database import update_mood, get_moods
from mood import tone_result
from weekly_mood import weekly_moods
from google_translate import google_translate
from watson import reload_watson_api

from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import json
import os
import requests
from discord.ext import commands
import random
from keepalive import keepalive

from discord.ext import commands
# enter token for the server
# TOKEN = os.environ['DISCORD_TOKEN'] # to use in repl

import discord
from discord.ext import commands, tasks

import datetime
import json
import random
import os


# ---

TEST = True

announcement_channels_list = []

try:
    with open('config/config.json') as config_file:
        conf = json.load(config_file)
    if conf['token'] is None:
        raise Exception
    token = conf['token']
    if TEST:
        token = conf['token_test']


except Exception:
    print("Failed to open config, check it exists and is valid.")

bot = commands.Bot(command_prefix='>', description="CheckinWithMe")

dmfailed = discord.Embed(
    title="DM Failed",
    description='',
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.from_rgb(240, 71, 71)
)

day_of_week = datetime.datetime.today().weekday()  # returns a number from 0 to 6
daily_motivation = [
    "Hey, I know it's Monday. But it's also a new day and a new week. "
    "And in that lies a new opportunity for something special to happen.",

    "Tuesday isn't so bad... It's a sign that I've somehow survived Monday.",

    "Wednesday is like small friday; half way to the weekend.",

    "Thankful Thursday, it's not happy people who are thankful. "
    "It's thankful people who are happy. Always look on the bright side of life",

    "TGIF!",

    "Saturday - it's a good day to have a good day!",

    "Sunday: A day to refuel your soul and be grateful for your blessings. "
    "Take a deep breath and realx. Enjoy your family, your friends and a cup of coffee."
]
days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Static

def update_announcement_list():
    global announcement_channels_list
    announcement_channels_list = []
    for guild in bot.guilds:
        for channel in guild.channels:
            if str(channel.type) == 'text':
                if str(channel.name) == "daily-check-in":
                    announcement_channels_list.append(channel)


def tone_response(tone, language="en"):
    # Switch statements couldn't come fast enough
    # TODO Switch statements on Python 3.10 release
    if tone:
        if tone == -1:
            return -1
        elif tone['tone_id'] == 'anger':
            return anger_response(language)
        elif tone['tone_id'] == 'fear':
            return fear_response(language)
        elif tone['tone_id'] == 'sadness':
            return sad_response(language)
        elif tone['tone_id'] == 'joy':
            return joy_response(language)
        else:
            return no_tone(language)
    else:
        return no_tone(language)


def joy_response(language):
    embed = discord.Embed(
        # Translate Title, if Language is English, Google Translate will not alter the string

        title=google_translate("It sounds like you're having an awesome day!", language)["translatedText"],
        description=google_translate("""Happiness looks different for everyone, but it is often described as involving """ + 
        """positive emotions and life satisfaction. Perhaps you've had a rough few days and things have just started """ +
        """to look up. Everyone experiences the ups and downs of life, but today is one of the good ones 😊.""", 
        language)["translatedText"],
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(252, 252, 153)
    )
    embed.add_field(name=google_translate("Advice", language)["translatedText"],
                    value=google_translate("""Take the time to do something you enjoy, develop positive habits or work """ +
                                           """towards one of your goals today to increase your happiness and """ +
                                           """life satisfaction in the long run. """ +
                                           """\nGive this article a read for tips to maintain happiness: """,
                                           language)["translatedText"])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name=google_translate("Resource", language)["translatedText"],
                    value=f"[{google_translate('10 Things Happy People Do to Stay Happy', language)['translatedText']}"
                          f"](https://tinybuddha.com/blog/10-things-happy-people-do-to-stay-happy/)")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
    return embed


def sad_response(language):
    embed = discord.Embed(
        title=google_translate("It looks like you might be feeling a little down.", language)["translatedText"],
        description=google_translate("We all feel sad at times. Sadness is a normal human emotion that can make life "
                                     "more interesting and teach us to appreciate happiness when it comes. That said, "
                                     "sadness can be overwhelming at times and lead us into a downward spiral if "
                                     "not dealt with. Here are some tips to work through sadness:",
                                     language)["translatedText"],
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(168, 228, 239)
    )

    embed.add_field(name=google_translate("Get out in nature", language)["translatedText"],
                    value=google_translate("Spending time outdoors can improve your mood and "
                                           "take your mind off your problems and widen your perspectives to beyond "
                                           "the current situation.", language)["translatedText"])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name=google_translate("Talk to someone.", language)["translatedText"],
                    value=google_translate("This could be a friend, therapist, or family member,"
                                           " someone you trust to listen to and comfort you if needed."
                                           " Many online services such as "
                                           "KidsHelpPhone also provide support for those in need.",
                                           language)["translatedText"])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name=google_translate("Take it one day at a time", language)["translatedText"],
                    value=google_translate("Do one thing to work towards improving your mental state today, "
                                           "such as going for a walk or connecting with an old friend. "
                                           "Do another tomorrow. Over time these little actions will build up.",
                                           language)["translatedText"])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name=google_translate("Give yourself time and permission to be sad", language)["translatedText"],
                    value=google_translate("Bottling up your feelings will do more harm than good over time. "
                                           "Don't be afraid to seek help or express your feelings through "
                                           "crying if you feel like it. ", language)["translatedText"])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name=google_translate("Remember, it will get better", language)["translatedText"],
                    value=google_translate("You may not feel like it now, but what may seem so significant "
                                           "today may not even matter in the future.", language)["translatedText"])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name=google_translate("Resource", language)["translatedText"],
                    value=f"[{google_translate('10 Ways to Cheer Yourself Up When You’re in a Bad Mood', language)['translatedText']}"
                          f"](https://www.lifehack.org/articles/lifestyle/10-ways-cheer-yourself-when-youre-bad-mood.html)")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845308432666853400/845752208297427034/logo_guy_but_sad.png")
    return embed


def anger_response(language):
    embed = discord.Embed(
        title=google_translate("I think you might be angry.", language)["translatedText"],
        description=google_translate("""Remember that it’s perfectly reasonable to get angry. """ +
        """Something that can help is letting out your anger and venting; holding it in can make it worse. """ +
        """Try out the resource below, or use `>resource` """ +
        """for some more great resources to help improve your mental health.""", language)["translatedText"],
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(251, 105, 98)
    )
    embed.add_field(name=google_translate("Resource", language)["translatedText"],
                    value=f"[{google_translate('How To Cool Off When Youre Angry', language)['translatedText']}"
                          f"](https://www.thehotline.org/resources/how-to-cool-off-when-youre-angry/)")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845308432666853400/845752208297427034/logo_guy_but_sad.png")
    return embed


def fear_response(language):
    embed = discord.Embed(
        title=google_translate("It looks like you’re experiencing fear/anxiety.", language)["translatedText"],
        description=google_translate("""I totally get that life can be overwhelming and stressful. """ + 
        """You might be able to get over your fears by trying to take a step back and distracting yourself. """ + 
        """You can often get in your own head and make your fears worse. """ + 
        """Try the resource below, or use `>resource` for some more great resources to help improve your mental health.""",
        language)["translatedText"],
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.from_rgb(168, 228, 239)
    )
    embed.add_field(name=google_translate("Resource", language)["translatedText"],
                    value=f"[**{google_translate('NHS Inform', language)['translatedText']}** - "
                          f"{google_translate('Ten Ways to Fight Your Fears', language)['translatedText']}]"
                          f"(https://www.nhsinform.scot/healthy-living/mental-wellbeing/fears-and-phobias/ten-ways-to-fight-your-fears)")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845308432666853400/845752208297427034/logo_guy_but_sad.png")
    return embed


def no_tone(language):
    embed = discord.Embed(title=google_translate("Oops!", language)['translatedText'],
                          description=google_translate("Sorry! I couldn't quite pinpoint how you are feeling. "
                                                       "Feel free to send me another message and "
                                                       "I'll try to figure out how you are feeling!",
                                                       language)["translatedText"],
                          timestamp=datetime.datetime.utcnow(),
                          color=discord.Color.from_rgb(61, 72, 73))

    embed.add_field(name=">rate", value=google_translate("You can also let me know how you are feeling with `>rate`!",
                                                         language)['translatedText'])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name=google_translate("Usage:", language)['translatedText'],
                    value="`>rate <Anger | Fear | Joy | Sadness>`")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name=google_translate("Example", language)['translatedText'],
                    value=google_translate("If I'm feeling happy, I would `>rate Joy` 😊", language)['translatedText'])
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
    return embed


def negative_ambiguous(language):
    embed = discord.Embed(
        title=google_translate("It looks like you might be feeling a little down.", language)['translatedText'],
        description=google_translate("We all have our ups and downs! Remember, sometimes, it's okay to not feel okay. "
                                     "Feel free to send me another message and "
                                     "I'll try to figure out how you are feeling!", language)['translatedText'],
        timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(153, 50, 204)
    )

    embed.add_field(name=">rate", value=google_translate("You can also let me know how you are feeling with `>rate`!",
                                                         language)['translatedText'])
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name=google_translate("Usage:", language)['translatedText'],
                    value="`>rate <Anger | Fear | Joy | Sadness>`")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name=google_translate("Example", language)['translatedText'],
                    value=google_translate("If I'm feeling happy, I would `>rate Joy` 😊", language)['translatedText'])
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845308432666853400/845752208297427034/logo_guy_but_sad.png")
    return embed


# Commands


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command(pass_context=True)
async def checkin(ctx, *, message=None):
    """
    Determines the user's mood by using IBM Watson's tone reader & Google Cloud's Natural Language Library
    and uploads it to the database.
    """
    if message:
        translate = google_translate(message)
        translation = translate["translatedText"]
        language = translate["detectedSourceLanguage"]
        tone = tone_result(translation)  # tone detection from ML libraries
        response = tone_response(tone, language)

        if tone:
            if response == -1:
                await ctx.send(embed=negative_ambiguous(language))
            elif response:
                my_tone = tone['tone_id']
                update_mood(ctx.message.author.id, my_tone)
                await ctx.send(embed=response)
            else:
                await ctx.send(embed=response)
        else:
            await ctx.send(embed=response)
    else:
        await ctx.send("Please follow `>checkin` with a description of how you're feeling!")


@bot.command(pass_context=True)
async def rate(ctx, *, message=None):
    """
    When the tone reader fails to determine a mood, the user can
    simply enter their mood and update the database with their mood
    """
    if message:
        rating = message.strip().lower()
        if rating in ["anger", "fear", 'joy', 'sadness']:
            tone = tone_result(rating)
            my_tone = tone['tone_id']
            update_mood(ctx.message.author.id, my_tone)
            response = tone_response(tone)
            await ctx.send(embed=response)
        else:
            embed = discord.Embed(title="Oops!", description="Sorry! I couldn't quite pinpoint how you are feeling. "
                                                             "Feel free to send me another message and "
                                                             "I'll try to figure out how you are feeling!",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(61, 72, 73))
            embed.add_field(name="Usage:", value="`>rate <Anger | Fear | Joy | Sadness>`")
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="Example", value="If I'm feeling happy, I would `>rate Joy` 😊")
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png"
            )
            await ctx.send(embed=embed)
    else:
        await ctx.send("Please follow `>rate` with a description of how you're feeling!")


@bot.command(pass_context=True)
async def commands(ctx):
    """
    Sends a list of the commands a user can use
    """
    embed = discord.Embed(title="List of Commands",
                          description="To use these commands, type '`>`' with the corresponding command.",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(226, 83, 47))
    embed.add_field(name="checkin", value="""> Let me know how you're feeling with the 'checkin' command! For """+ 
                    """instance, you could type `>checkin I'm feeling pretty happy today` or any other feelings you have.\n\n""" +
                    """> Your mood will then be categorized into one of four categories (anger, fear, joy, and sadness) """ +
                    """and will be compiled in a weekly summary for you to view at anytime."""
                    )
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="rate", value="""> You can also let me know how you are feeling with the 'rate' command! 
    > Please include one of the following: `| Anger | Fear | Joy | Sadness |` with the command.\n\n""" +
    """> This provides a more direct and accurate method for our systems to track your mood."""
                    )
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="history", value="> Sends you a summary graphic of your mood over the last seven days.")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="motivation", value="> Sends motivational messages to cheer you on to bigger and better.")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')

    embed.add_field(name="resource", value="> Generates a random resource to help you develop your mental health!")

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
    await ctx.send(embed=embed)


@bot.command()
async def motivation(ctx):
    """
    Calls get_motivation() and which gets a reddit post from the top of r/GetMotivated
    """
    motivation_url = get_motivation()
    await ctx.send(motivation_url)


@bot.command()
async def resource(ctx):
    """
    Sends a random resource from a list of mental health resources
    """
    resources = [
        "https://www.mindful.org/meditation/mindfulness-getting-started/",
        "https://www.mindful.org/how-to-meditate/",
        "https://www.youtube.com/watch?v=inpok4MKVLM",
        "https://gratefulness.org/",
        "https://www.helpguide.org/articles/healthy-living/the-mental-health-benefits-of-exercise.htm",
        "https://www.youtube.com/c/HealthyGamerGG/videos",
        "https://psychcentral.com/",
        "https://headtohealth.gov.au/",
        "https://www.calmsage.com/",
        "https://www.loveisrespect.org/resources/self-care-when-youre-angry/",
        "https://www.youtube.com/playlist?list=PLQiGxGHwiuD1kdxsWKFuhE0rITIXe-7yC",
        "https://reallifecounseling.us/overcome-fear-and-anxiety/"
    ]
    resource = random.choice(resources)
    embed = discord.Embed(title="Random Resource", description=resource, timestamp=datetime.datetime.utcnow(),
                          color=discord.Color.from_rgb(226, 83, 47))
    await ctx.send(embed=embed)


@bot.command()
async def history(ctx):
    """
    Uploads a graphic sunmmarizing your mood over the past seven days.
    """
    user_id = ctx.message.author.id
    weekly_moods(get_moods(user_id), user_id)
    await ctx.send(file=discord.File(f'process/{user_id}.png'))
    os.remove(f'process/{user_id}.png')


# Events

@bot.event
async def on_guild_join(guild):
    """
    Activates as the bot joins a discord server. 
    It sets its server permissions, creates a channel for daily checkins, sends an introductory
    message, and sends the first daily checkin reminder.
    """
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True),
        guild.default_role: discord.PermissionOverwrite(send_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        guild.me: discord.PermissionOverwrite(send_messages=True),
    }
    await guild.create_text_channel('daily-check-in', overwrites=overwrites)
    channel_id = discord.utils.get(guild.channels, name='daily-check-in').id
    channel = bot.get_channel(channel_id)
    update_announcement_list()
    embed = discord.Embed(title="Hello World! 👋",
                          description="""My name is Pip and I'm here to help you track your moods on the daily.""",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(255, 255, 77))
    embed.add_field(name="How I work",
                    value="> All you have to do is tell me how you're doing each day by *sending me a message*, "
                          "and a graphic from the last seven days will be compiled for you to view at anytime."
                          " Understanding and monitoring your moods is crucial to "
                          "managing them and feeling better faster. If you are "
                          "more aware of your moods, you may be able to better manage your lifestyle choices, " 
                          "make informed health decisions, prevent or avoid triggers of negative moods, " 
                          "and work towards a better quality of life. Best of luck on your mental health journey!" 
                          "\n\nTo see a list of commands, type `>commands`!")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
    await channel.send(embed=embed)

    embed = discord.Embed(title=f"⭐ Happy {days_of_the_week[day_of_week]}! ⭐",
                          description="> Yesterday is history. "
                                      "Tomorrow is a mystery, but today is a gift! "
                                      "That is why it is called the present.",
                          timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(221, 160, 51))
    embed.add_field(name="Check in With Me!", value=f"{bot_tag.mention}")
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name='\u200b', value='\u200b')
    embed.add_field(name="Daily Motivation", value=daily_motivation[day_of_week])
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
    await channel.send(embed=embed)


@bot.event
async def on_ready():
    if not os.path.exists('process'):
        os.mkdir('process')
    await bot.change_presence(activity=discord.Game("Let's check in! | prefix: >"), status="online")
    global bot_tag
    bot_tag = bot.user
    update_announcement_list()
    refresh_reddit_token()
    reload_watson_api()
    print('Bot Initialized')


# Tasks

@tasks.loop(hours=1)
async def reload_tokens():
    """
    refreshes Reddit & Watson access token every hour
    """
    refresh_reddit_token()
    reload_watson_api()


@tasks.loop(hours=24)
async def checkin_announcement():
    """
    Sends a reminder every 24 hours to users to remind them to checkin and track their mood
    """
    day_of_week = datetime.datetime.today().weekday()
    for channel in announcement_channels_list:
        embed = discord.Embed(title=f"⭐ Happy {days_of_the_week[day_of_week]}! ⭐",
                              description="> Yesterday is history. "
                                          "Tomorrow is a mystery, but today is a gift! "
                                          "That is why it is called the present.",
                              timestamp=datetime.datetime.utcnow(), color=discord.Color.from_rgb(221, 160, 51))
        embed.add_field(name="Check in With Me!", value=f"{bot_tag.mention}")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="Daily Motivation", value=daily_motivation[day_of_week])
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/845318994666848261/845399136249053205/logo_guy.png")
        await channel.send(embed=embed)

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # for dev purpose

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# ---------------------BOT COMMAND
bot = commands.Bot(command_prefix='!')
# ---------------------WEB SCRAPING
scraping = open("faq.json", encoding="UTF-8")
scraped = json.load(scraping)
# ----------------FOR HELPLINE
helplines = ["Family Violence Prevention Center 1-800-313-1310",
             "National Sexual Assault Hotline 1-800-656-HOPE (4673)",
             "Drug Abuse National Helpline 1-800-662-4357",
             "American Cancer Society 1-800-227-2345",
             "Eating Disorders Awareness and Prevention 1-800-931-2237",
             "GriefShare 1-800-395-5755",
             "Suicide Hotline 1-800-SUICIDE (784-2433)"]

@bot.command(aliases=['event', 'nextevent', 'nextevents', 'upcomingevent', 'upcomingevents'], help='Get a list of the ongoing and upcoming events of the pod. Enter the count of events to retrieve following the command. It\'s default value is 1.')
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


@bot.command(name='faq', help="\
    Searches the FAQ for the most relevant section corresponding to the provided keyword. List of keywords: \
    - 😄 **MLHintro** - For in depth introduction to MLH fellowship. \
    - 🌲 **MLHevents**- What are MLH events? Know everything about them. \
    - 🚂 **pods** - What are pods? Know everything here \
    - 📱 **discord** -How to use discord and which channel serves what purpose \
    - 📞 **zoom**- What is zoom used for? \
    - 📢 **feedback** - What is feedback in MLH? \
    - ⏰ **remote** - How to work remotely and give your 100% in MLH. \
    - 📏 **hackathonrules** - Rules for hackathons \
    - 🥇 **hackjudge** - How do judges make a decision for hackathon winner? What is taken into consideration? \
    - 💯 **hackdemo** - How to prepare a good demo for hackathon? \
    - 🙋 **attendance** - What is the importance of attendance in MLH and how is it monitored?\
    - 💁 **expectations** - What MLH expects from you as fellows\
    - ⛑️ **help** - Facing problems in MLH? Reach out to us\
")
async def faq(ctx, keyword):
    for i in scraped["intents"]:
        if(keyword==i["tag"]):
            quote = i["responses"]
    # response = quote
    for i in quote:
        response = i
        await ctx.send(response)


@bot.command(aliases=['al'], help="Get all helpline numbers related to mental health")
async def all(ctx):
    for i in helplines:
        res = i
        await ctx.send(res)

@bot.command(aliases=['depression'], help="Get helpline number to tackle depression and suicidal thoughts")
async def suicide(ctx):
    await ctx.send(helplines[6])

@bot.command(aliases=['violent'], help="Get helpline number to tackle violence")
async def violence(ctx):
    await ctx.send(helplines[0])

@bot.command(aliases=['drugs'], help="Get helpline number to tackle drug addiction")
async def drugabuse(ctx):
    await ctx.send(helplines[2])

@bot.command(aliases=['assault'], help="Get helpline number to tackle assaults")
async def sexualAssault(ctx):
    await ctx.send(helplines[1])

@bot.command(aliases=['ILLNESS'], help="Get helpline number to tackle illness")
async def cancer(ctx):
    await ctx.send(helplines[3])

@bot.command(aliases=['sorrow'], help="Get helpline number to tackle grief")
async def grief(ctx):
    await ctx.send(helplines[5])

@bot.command(aliases=['eating'], help="Get helpline number to tackle eating disorder")
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

checkin_announcement.start()
reload_tokens.start()

# ---------------------INITIALIZING THE BOT
bot.run(TOKEN)
