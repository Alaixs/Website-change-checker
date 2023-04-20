# Website-change-checker
A discord bot and a python script that runs on rapsberry pi os Lite that allows to check if the content of a div of a website is different and that warns you on discord

## Setup

### For the discord part :
- You need to put your **bot token** in discordBot.py file 
- A **webhook url** in discordBot.py and checker.py file 
 
 ### For the site to monitor:
- You need to put your **url and the div** to monitor in checker.py. The code is very flexible you can monitor what you want.

## How does it work?

Start your main.py and discordBot.py
Once this is done main will make sure that your script does not stop even if the site bugs and makes your script spit.
**discordBot.py** will allow you to make sure that your bot is still running and to have information like the number of requests made or when it made its last request.
**Checker.py** will warn you thanks to the webhook by sending a notification as soon as the page has had a change on the div.

## Warning

You should only use this script on sites that allow this kind of practice.
The script is likely to return false positives especially on sites using js to generate html
