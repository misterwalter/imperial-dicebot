import discord
import asyncio
import random
import re

# Load account token from other file
token = open("token", "r").read().strip()


# Global Initializations
client = discord.Client()
# Note that any roll with more than 300ish dice is going to fail to send anyway
check_regex = re.compile("^[rcy](\d{1,3})(.*)", re.IGNORECASE)
save_regex = re.compile("^[ns](\d{1,3})(.*)", re.IGNORECASE)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('--------')


@client.event
async def on_message(message):
    print("{}:{}{}:{}".format(
        message.author,
        message.server.name+":" if message.server else "",
        message.channel,
        message.content,
    ))
    # Roll a check (success on 3-6)
    if check_regex.match(message.content):
        m = check_regex.match(message.content)
        results = ""
        score = 0
        for i in range(int(m.group(1))):
            die = random.randrange(1, 7)
            if die > 2:
                score += 1
                results += " **[{}]**".format(die)
            else:
                results += "[{}]".format(die)
        subject = m.group(2)
        subject = " re: " + subject if subject else ""
        await client.send_message(
                message.channel,
                "**{0}** got {1} successes {2} on their **Check**{3}".format(
                    message.author.display_name,
                    score,
                    results,
                    subject
                ))
    # Roll a save (success on 4-6)
    elif save_regex.match(message.content):
        m = save_regex.match(message.content)
        results = ""
        score = 0
        for i in range(int(m.group(1))):
            die = random.randrange(1, 7)
            if die > 3:
                score += 1
                results += " **[{}]**".format(die)
            else:
                results += "[{}]".format(die)

        subject = m.group(2)
        subject = " re: " + subject if subject else ""
        await client.send_message(
                message.channel,
                "**{0}** got {1} successes {2} on their **Save**{3}".format(
                    message.author.display_name,
                    score,
                    results,
                    subject
                ))
    # Mindless trolling
    elif "now" in message.content.lower():
        await slow_talk(
            message,
            "Now, don't be hasty young {}.".format(message.author.mention)
        )


# Not currently used but I wanted AW to see a fun thing.
async def slow_talk(message, response):
    msg = await client.send_message(message.channel, "hmmmmmmmmm...")
    await asyncio.sleep(5)
    for i in range(len(response)+1):
        await client.edit_message(msg, response[:i])
        await asyncio.sleep(2)


# Actually kicks things off
client.run(token)
