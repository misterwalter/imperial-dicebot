# Imperial Dicebot
A Discord.py die rolling bot for Imperial Dawn, an excellent tabletop RPG

The game itself is available for free at https://imperialdawn.com

This uses the discord.py library available at https://github.com/Rapptz/discord.py, which is pretty great all things considered, especially for setting up simple bots.

# Bootstrapping
When first setting up the bot, be sure to run the ./bootstrap.sh file, as it will do a few handy things for you:
- Create an example **bot_admin** file. This file should contain the mention tag of the whoever you want to be able to control the bot. The current tag is invalid, but looks a bit like a real mention tag.
- Create an example **token** file. This file should contain your bot's login token, not their Client ID or Client secret.
- Create a default **report_format** file. This file contains a default format for DiceReport records that I think looks nice enough, but can be edited at your option. I find myself tweaking it often, and now you can too.

# Running
While not super satisfying to use, the dicebot.sh script will restart your bot in case it crashes. This is unfortunately useful, as errors that I don't yet understand seem to come through sometimes, especially when working over a spotty connection. The bot is reliable over a good connection though, and in my experience a spotty one only caused issues on a week to week basis, not a minute to minute one.

# Sharing and Feedback
This code should be considered free to use or learn from by anyone, attribution and notification is preferred if appropriate but not required. There's probably an official license that says that, but I don't feel like digging through contracts right now, and realistically nobody's gonna rip off a bot this simple. I probably wouldn't even care if they did. I mostly just want to hear from you if you get anything out of this, that would really make my day.

I'd love to hear any suggestions for usability or reliability improvements, please feel free to leave a comment, issue, etc.
