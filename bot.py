## Dicebot made originally for Imperial Dawn, one of the better TTRPGs

from collections import defaultdict
import random
import re

import discord

from player_stats import PlayerStats

dawn_regex = re.compile("^r(\d{1,3})(.*)", re.IGNORECASE)       ## Rolling Imperial Dawn Dice r3, r8, r9k, etc
generic_regex = re.compile("^(\\d{0,8})d(\\d+)\s*([+-]\s*\\d+)?(,*)", re.IGNORECASE)
dice_manager_dict = defaultdict(PlayerStats)

class ImperialClient(discord.Client):
    async def on_ready(self):
        print("Logged and Loaded as", self.user)

    def roll_die(self, sides : int, mention : str) -> int:
        result = random.randrange(1, sides+1)
        print(f"{mention} rolled a {result} out of {sides}")

        dice_manager_dict[mention].score_per_side[sides] += result
        dice_manager_dict[mention].dice_per_side[sides] += 1
        dice_manager_dict["Everyone"].score_per_side[sides] += result
        dice_manager_dict["Everyone"].dice_per_side[sides] += 1

        return result


    async def on_message(self, message):
        print("{}:{}{}:{}".format(
            message.author,
            message.guild.name+":" if message.guild else "",
            message.channel,
            message.content,
        ))
        if message.author == self.user:
            return
        
        if message.content == "o/":
            await message.channel.send("\\o")

        ## Regexs first as they are fast and it's casual coding time
        dawn_match = dawn_regex.match(message.content)
        generic_match = generic_regex.match(message.content)

        ## ID rolling
        print(generic_match)
        # print(message.author.mention)
        # print(self.admin)
        # IMPERIAL DAWN DICE ROLLS ===========================================
        if dawn_match:
            results = ""
            score = 0
            dice_count = int(dawn_match.group(1))
            for i in range(dice_count):
                die = self.roll_die(6, message.author.mention)
                if die >= 3:
                    score += 1
                    results += f" **[{die}]**"
                else:
                    results += f" [{die}]"


            ## Final Formatting
            if len(results) > 400:
                results = "[lots of dice]"
            memo = dawn_match.group(2)
            memo = f"re: {memo}" if memo else ""

            await message.channel.send(f"**{message.author.mention}** got {score} successes {results}{memo}")
        # GENERIC DICE ROLLS =================================================
        elif generic_match:
            results = ""
            dice = int(generic_match.group(1).replace(" ", "")) if generic_match.group(1) else 1
            sides = int(generic_match.group(2))
            bonus = int(generic_match.group(3).replace(" ", "")) if generic_match.group(3) else 0
            score = bonus ## Final +/- is a good place to start scoring
            for i in range(dice):
                roll_score = self.roll_die(sides, message.author.mention)
                score += roll_score
                results = f"{results}[{roll_score}]"


            ## Final Formatting
            if len(results) > 400:
                results = "[lots of dice]"
            memo = generic_match.group(4)
            memo = f"re: {memo}" if memo else ""

            await message.channel.send(f"{message.author.mention} rolled {results}\nTotal: {score} {memo}")
        elif message.content.startswith("!reset") and message.author.mention == self.admin:
            dice_manager_dict.clear()
            await message.channel.send(f"I kill at your command, {self.admin}!\no7")
        elif message.content.startswith("!report"):
            admin_call = message.author.mention == self.admin       ## Only admin can get reports on everyone bc it does ping people
            for mention, record in dice_manager_dict.items():
                if admin_call or mention == message.author.mention:
                    await message.channel.send(record.get_report(mention))



    def activate(self):
        with open(".token", "r") as file:
            token = file.read().strip()
        with open(".admin", "r") as file:
            self.admin = file.read().strip()
        self.run(token)

intents = discord.Intents.default()
intents.message_content = True
client = ImperialClient(intents=intents)
client.activate()