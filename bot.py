## Dicebot made originally for Imperial Dawn, one of the better TTRPGs

import discord


class ImperialClient(discord.Client):
    async def on_ready(self):
        print("Logged and Loaded as", self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content == "o/":
            await message.channel.send("\o")

    def activate(self):
        with open(".token", "r") as file:
            token = file.read().strip()
            print(token)
        print(token)
        self.run(token)

intents = discord.Intents.default()
intents.message_content = True
client = ImperialClient(intents=intents)
client.activate()