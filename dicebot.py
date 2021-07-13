import discord
import asyncio
from collections import defaultdict
import random
import re

# Load account token from other file
token = open("token", "r").read().strip()
# List of admins for the dicebot, described elsewhere
bot_admin = open("bot_admin", "r").read().strip()
# Used as a formatted string for posting reports
report_format = open("report_format", "r").read()

# Regular expression for detecting Imperial Dawn rolls.
dawn_regex = re.compile("^r(\d{1,3})(.*)", re.IGNORECASE)
#Regular expression for detecting generic dice rolls.
generic_regex = re.compile("^(\d{0,8})d(\d+)\s*([+-]\s*\d+)?(.*)", re.IGNORECASE)


class DiceRecord:
    """
    A record of a player's luck and speech throughout a session.
    Note that the players name is not stored here,
    it is the key by which the DiceRecord is accessed.
    """

    def __init__(self):
        self.successes = 0
        self.dice = 0
        self.rolls = 0

    # returns a string of all rolling stats according to a config file
    def display_rolling_stats(self, mention):
        accuracy = 0 if self.dice == 0 else 100*self.successes/self.dice
        efficiency = 0 if self.rolls == 0 else self.dice/self.rolls
        return report_format.format(
            mention=mention,
            successes=self.successes,
            dice=self.dice,
            rolls=self.rolls,
            accuracy=accuracy,
            efficiency=efficiency,
        )

# Global Initializations
client = discord.Client()
dice_manager_dict = defaultdict(DiceRecord)


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
        message.guild.name+":" if message.guild else "",
        message.channel,
        message.content,
    ))
    lower = message.content.lower()
    # Roll a check (success on 2-6)
    if dawn_regex.match(message.content):
        m = dawn_regex.match(message.content)
        results = ""
        score = 0
        dice = int(m.group(1))
        for i in range(dice):
            die = random.randrange(1, 7)
            if die >= 3:
                score += 1
                results += " **[{}]**".format(die)
            else:
                results += "[{}]".format(die)
        memo = m.group(2)
        dice_manager_dict[message.author.mention].successes += score
        dice_manager_dict[message.author.mention].dice += dice
        dice_manager_dict[message.author.mention].rolls += 1

        dice_manager_dict["Everyone"].successes += score
        dice_manager_dict["Everyone"].dice += dice
        dice_manager_dict["Everyone"].rolls += 1

        memo = " re: " + memo if memo else ""
        await message.channel.send(
                "**{0}** got {1} successes {2}{3}".format(
                    message.author.mention,
                    score,
                    results,
                    memo
                ))
    # Roll a generic roll
    elif generic_regex.match(message.content):
        m = generic_regex.match(message.content)
        results = ""
        dice = int(m.group(1).replace(" ", "")) if m.group(1) else 1
        sides = int(m.group(2))
        score = int(m.group(3).replace(" ", "")) if m.group(3) else 0
        for i in range(dice):
            die = random.randrange(1, sides+1)
            score += die
            if dice < 300:
                results += "[{}]".format(die)

        memo = m.group(4)

        if len(results) > 400:
            results = "[lots of dice]"

        memo = " re:" + memo if memo else ""
        await message.channel.send(
                "**{0}** rolled{1} {2}\nTotal: **{3}** {4}".format(
                    message.author.display_name,
                    " " + results if results else "",
                    m.group(3).replace(" ", "") if m.group(3) else "",
                    score,
                    memo,
                ))
    elif "!reset" in lower and message.author.mention == bot_admin:
            dice_manager_dict.clear()
    elif "!report" in lower and message.author.mention == bot_admin:
        print("REPORTED")
        for mention, record in dice_manager_dict.items():
            print("MODS")
            await message.channel.send(
                record.display_rolling_stats(mention),
            )

# Actually kicks things off
client.run(token)
