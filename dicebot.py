import discord
import asyncio
from collections import defaultdict
import random
import re

# Load account token from other file
token = open("token", "r").read().strip()
bot_admin = open("bot_admin", "r").read().strip()
report_format = open("report_format", "r").read()


class DiceRecord:
    """
    A record of a player's luck and speech throughout a session.
    Note that the players name is not stored here,
    it is the key by which the DiceRecord is accessed.
    """

    def __init__(self):
        self.check_successes = 0
        self.check_dice = 0
        self.check_rolls = 0
        self.save_successes = 0
        self.save_dice = 0
        self.save_rolls = 0
        self.words = defaultdict(int)

    # Adds the words spoken by a player to a list of words spoken
    def record_text(self, sentence):
        punctuation = '''!()-[]{};:'"\,<>./?@#$%^'''
        clean_sentence = "".join(c for c in sentence if c not in punctuation)
        word_list = [word.strip() for word in clean_sentence.split(' ')]
        for word in word_list:
            self.words[word] += 1

    # returns a string of all rolling stats according to a config file
    def display_rolling_stats(self, mention):
        check_accuracy = 0 if self.check_dice is 0 else 100*self.check_successes/self.check_dice
        check_efficiency = 0 if self.check_rolls is 0 else self.check_dice/self.check_rolls
        save_accuracy = 0 if self.save_dice is 0 else 100*self.save_successes/self.save_dice
        save_efficiency = 0 if self.save_rolls is 0 else self.save_dice/self.save_rolls
        return report_format.format(
            mention=mention,
            check_successes=self.check_successes,
            check_dice=self.check_dice,
            check_rolls=self.check_rolls,
            check_accuracy=check_accuracy,
            check_efficiency=check_efficiency,
            save_successes=self.save_successes,
            save_dice=self.save_dice,
            save_rolls=self.save_rolls,
            save_accuracy=save_accuracy,
            save_efficiency=save_efficiency,
        )

    # returns  list of the most commonly used words, truncated to any length.
    def list_top_words(self, word_count):
        inv_dict = defaultdict(list)
        [inv_dict[word].append(word) for word, count in self.words.items()]
        word_list = list(inv_dict.keys())
        word_list.sort()
        word_list = [inv_dict[num] for num in word_list]
        final_list = []
        [final_list.extend(sub_list) for sub_list in word_list[-word_count:]]
        final_list = final_list[-word_count:]
        return final_list


# Global Initializations
client = discord.Client()
dice_manager_dict = defaultdict(DiceRecord)
dice_manager_dict["Everyone"]
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
    lower = message.content.lower()
    # Roll a check (success on 3-6)
    if check_regex.match(message.content):
        m = check_regex.match(message.content)
        results = ""
        score = 0
        dice = int(m.group(1))
        for i in range(dice):
            die = random.randrange(1, 7)
            if die > 2:
                score += 1
                results += " **[{}]**".format(die)
            else:
                results += "[{}]".format(die)
        subject = m.group(2)
        dice_manager_dict[message.author.mention].check_successes += score
        dice_manager_dict[message.author.mention].check_dice += dice
        dice_manager_dict[message.author.mention].check_rolls += 1

        dice_manager_dict["Everyone"].check_successes += score
        dice_manager_dict["Everyone"].check_dice += dice
        dice_manager_dict["Everyone"].check_rolls += 1

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
        dice = int(m.group(1))
        for i in range(dice):
            die = random.randrange(1, 7)
            if die > 3:
                score += 1
                results += " **[{}]**".format(die)
            else:
                results += "[{}]".format(die)

        subject = m.group(2)
        dice_manager_dict[message.author.mention].save_successes += score
        dice_manager_dict[message.author.mention].save_dice += dice
        dice_manager_dict[message.author.mention].save_rolls += 1

        dice_manager_dict["Everyone"].save_successes += score
        dice_manager_dict["Everyone"].save_dice += dice
        dice_manager_dict["Everyone"].save_rolls += 1

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
    elif "now" in lower and random.randrange(1, 10) is 1:
        await slow_talk(
            message,
            "Now, don't be hasty young {}.".format(message.author.mention)
        )
    elif "!reset" in lower and message.author.mention == bot_admin:
            dice_manager_dict.clear()
    elif "!report" in lower and message.author.mention == bot_admin:
        for mention, record in dice_manager_dict.items():
            await client.send_message(
                message.channel,
                record.display_rolling_stats(mention),
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
