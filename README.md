# Imperial Dicebot
A Discord.py die rolling bot for Imperial Dawn, an excellent tabletop RPG

The game itself is available for free at https://imperialdawn.com

This uses the discord.py library available at https://github.com/Rapptz/discord.py, which is pretty great all things considered, especially for setting up simple bots.

# Basic Use
To roll a check, type either r, c, or y (corresponding to Roll, Check, or Yes) immedidately followed by a number, like so:

 - `c3`  ->  **Tdomo Dau** got 3 successes  **[4]**[1] **[3]** on their Check
 - `r4 throw gallon of boi`  ->  **Tosser** got 3 successes  **[4]**[1] **[3]** **[6]** on their Check re:  throw gallon of boi

A Save can be rolled in a similar fashion, using s or n (Save or No):

 - `s2 pls no`  ->  **Civi** got 0 successes [1][2] on their Save re:  pls no
 - `n6 dance away gracefully`  ->  **Senulous the Smooth** got 5 successes **[5]** **[4]** **[6]**[3] **[4]** **[6]** on their Save re: dance away gracefully

As you can see, adding more text to end of the message beyond the roll specification simply leaves a note on the end of the response, which can be handy and fun.

# Add To Your Server
To simply add this bot to your server as is, [have a server admin click this link](https://discordapp.com/oauth2/authorize?client_id=376921158420791297&scope=bot&permissions=285760) and authorize the bot on that server. This adds the instance that I run on my servers to your server as well, instead of going through the trouble of running your own bot. It will be sufficient for most basic purposes, you just won't be able to use the !report feature, because you won't be in my bot_admin file.

Not all requested permissions are currently used, but given that it's impossible for me to ask for more permissions later, I opted to ask for them now. Feel free to not check all the boxes.

# Bootstrapping
When first setting up your own instance of the bot, be sure to run the ./bootstrap.sh file, as it will do a few handy things for you:
- Create an example **bot_admin** file. This file should contain the mention tag of the whoever you want to be able to run the !report and !reset functions. The default tag is invalid, but looks a bit like a real mention tag does when not displayed on the client. If you're having trouble figuring out your mention tag, just have the bot print out all messages that it sees, and then tag yourself.
- Create an example **token** file. This file should contain your bot's login token, not their Client ID or Client secret.
- Create a default **report_format** file. This file contains a default format for DiceReport records that I think looks nice enough, but can be edited at your option. I find myself tweaking it often, and now you can too.

# Running
Running the diceloop.sh script instead of having python execute the dicebot.py file will restart your bot in case it crashes. This is particularly useful when working over a spotty connection, which seems to be a pain point for discord.py. The bot is quite reliable over a good connection, but seeing as I've already written the diceloop.sh script you might as well just use it regardless of your connection quality.

# Sharing and Feedback
This code should be considered free to use or learn from by anyone, attribution and notification is preferred if appropriate but not required. There's probably an official license that says that, I just don't feel like digging through contracts, and realistically nobody's gonna rip off a bot this simple. I probably wouldn't even care if they did. I mostly just want to hear from you if you get anything out of this, that would really make my day.

I'd love to hear any suggestions for usability or reliability improvements, please feel free to leave a comment, issue, etc.
