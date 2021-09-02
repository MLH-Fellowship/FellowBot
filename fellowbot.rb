require 'discordrb'
config = File.foreach('config.txt').map { |line| line.split(' ').join(' ') }
token = config[0].to_s
bot = Discordrb::Commands::CommandBot.new token: "#{token}", client_id: "#{config[1].to_s}", prefix: "#{config[2].to_s}"

helplines = ["Family Violence Prevention Center 1-800-313-1310",
             "National Sexual Assault Hotline 1-800-656-HOPE (4673)",
             "Drug Abuse National Helpline 1-800-662-4357",
             "American Cancer Society 1-800-227-2345",
             "Eating Disorders Awareness and Prevention 1-800-931-2237",
             "GriefShare 1-800-395-5755",
             "Suicide Hotline 1-800-SUICIDE (784-2433)"]

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
    "I can understand totally. But do you know how can you cope up?. Let me help you : 1. Divide your time into blocks",
    "and make sure you are being generous to yourself.",
    "2. Make sure you drink enough water and go out for a walk when your mind gets cluttered.",
    "3. A little music does not hurt anyone.",
    "4. We as coders feel as impostors all the time, don't worry just make sure you have faith on yourself",
    "I can totally understand, have you ever tried the pomodore technique.? Read about it here - https://en.wikipedia.org/wiki/Pomodoro_Technique#:~:text=The%20Pomodoro%20Technique%20is%20a%20time%20management%20method,25%20minutes%20in%20length%2C%20separated%20by%20short%20breaks. "
]

positivereply = [
    "We are extremely sorry to hear that you feel like this , but you are not alone in this. We as MLH put your well being as the top priority. Come talk to us what is bothering you. Help is available, speak with a counselor today by calling the National Suicide Prevention Lifeline at 800-273-8255",
    "WE ARE THERE FOR YOU!!. When you think life isn't worth it, search for some new options. Help is available, speak with a counselor today by calling the National Suicide Prevention Lifeline at 800-273-8255"
]
bot.command :ping do |msg|
    msg.respond "pong."
end 

bot.command :test do |event|
    event.respond helplines[0]
end

bot.message(start_with: '!game') do |event|

    magic = rand(1..10)
  
    event.respond "Can you guess my secret number? It's between 1 and 10!"
    event.user.await!(timeout: 300) do |guess_event|
      guess = guess_event.message.content.to_i
  
      if guess == magic
        guess_event.respond 'you win!'
        true
      else
        guess_event.respond(guess > magic ? 'too high' : 'too low')
        false
      end
    end
    event.respond "My number was: `#{magic}`."
  end
  
  
CROSS_MARK = "\u274c"
  
  
bot.message(content: '!time') do |event|
    message = event.respond "The current time is: #{Time.now.strftime('%F %T %Z')}"
  
    message.react CROSS_MARK
    bot.add_await!(Discordrb::Events::ReactionAddEvent, message: message, emoji: CROSS_MARK, timeout: 30) do |_reaction_event|
      message.delete 
    end
    puts 'Await destroyed.'
  end
  
bot.message(contains: sad_words) do |event|
    event.respond 
end 
bot.run

# @bot.event
# async def on_message(message):
#     flag = False
#     gify = False
#     await bot.process_commands(message)
#     msg = message.content
#     if message.author == bot.user:
#         return
#     if any(word in msg for word in greetings):
#         gify = True
#         response = random.choice(greet)
#         await message.channel.send(response)

#     if any(word in msg for word in sad_words):
#         flag = True
#         response = random.choice(starter_encouragements)
#         await message.channel.send(response)

#     if any(word in msg for word in problems):
#         flag = True
#         response = random.choice(copeup)
#         await message.channel.send(response)

#     if any(word in msg for word in suicide):
#         flag = True
#         response = random.choice(positivereply)
#         await message.channel.send(response)

#     if(flag):
#         r1 = "And just to brighten your day, here is a joke for you"
#         await message.channel.send(r1)
#         r2 = joke()
#         await message.channel.send(r2)

#     if 'quote' in msg.lower():
#         response = get_qoute()
#         await message.channel.send(response)


# @bot.command(name='faq', help="\
