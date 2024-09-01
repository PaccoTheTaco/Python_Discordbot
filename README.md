## English version below

## Deutsch:
### Hier sind ein paar Eindrücke was man mit dem Bot ales machen kann: 

Giveaways: 

![giveaways](/example_pics/giveaway.png)
![end giveaway](/example_pics/end_giveaway.png)

Es gibt auch Commands für den Spaß: 

![fun](/example_pics/fun.png)

Der standart /ping Command dafür natürlich nicht fehlen, dieser zeigt die Latenzzeit:

![ping](/example_pics/pings.png)

Um diesen Bot selber laufen lassen zu können muss man folgende Schritte machen:
- falls du noch keinen Discordbot hast dann erstelle im [Discord Developer Portal](https://discord.com/developers/applications) einen Bot
- lade die neuste ZIP datei von der ![Release Seite](https://github.com/PaccoTheTaco/Python_Discordbot/releases) herunter
- entpacke die zip und speichere den Ordner auf deinem Server
- installiere Python wenn du es noch nicht hast (sudo apt install python3)
- installiere dir nun pip wenn du es noch nicht hast (sudo apt-get install python3-pip)
- installiere über pip die benögten Pakete (pip install -r requirements.txt)
- in dem Verzeichnis wo die Datei "bot.py" liegt erstellst du nun die Datei .env 
- in die .env Datei schreibst du nun "DISCORD_BOT_TOKEN=(hier token vom Developer Portal einfügen)"
- nun müssen noch die IDs getauscht werden: welcome.py --> channel_id; leave.py --> channel_id; logs.py --> log_channel_id
- Jetzt kannst du deinen Bot in der cmd mit dem Befehl "python3 bot.py" starten

-----------------------

## English:
### Here are a few impressions of what you can do with the bot: 

Giveaways: 

![giveaways](/example_pics/giveaway.png)
![end giveaway](/example_pics/end_giveaway.png)

There are also commands for fun: 

![fun](/example_pics/fun.png)

The standard /ping command for this is of course not missing, this shows the latency time:

![ping](/example_pics/pings.png)

To run this bot yourself you have to do the following steps:
- if you don't have a Discordbot yet then create a bot in the [Discord Developer Portal](https://discord.com/developers/applications)
- download the latest ZIP file from the ![Release Page](https://github.com/PaccoTheTaco/Python_Discordbot/releases)
- extract the zip and save the folder on your server
- install python if you don't have it yet (sudo apt install python3)
- now install pip if you don't have it yet (sudo apt-get install python3-pip)
- install the required packages via pip (pip install -r requirements.txt)
- in the directory where the file ‘bot.py’ is located, create the file .env 
- in the .env file write ‘DISCORD_BOT_TOKEN=(insert token from Developer Portal here)’
- Now the IDs have to be swapped: welcome.py --> channel_id; leave.py --> channel_id; logs.py --> log_channel_id
- Now you can start your bot in the cmd with the command ‘python3 bot.py’