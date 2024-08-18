English version below

Deutsch:
Um diesen Bot selber laufen lassen zu können muss man folgende Schritte machen:
- im Discord developer Portal (https://discord.com/developers/applications) eine neue Application erstellen
--> https://screens.paccothetaco.com/ScreensX/2024/08/18/Southernhairnosedwombat_rVDbu8adVo.jpg
- falls noch nicht vorhanden dann muss dotenv installiert werden (pip install python-dotenv)
- im Code, im gleichen Pfad wo auch bot.py liegt die Datei .env erstellen
- im Discord Developer Portal unter dem Punkt Settings --> Bot, ist ein Button mit "Reset Token", wenn dieser gedruckt wurde muss man nochmal verifizieren das man auch wirklich der BEseitzer des Accounts ist und danach bekommt man einen Token und darunter erscheint der Button "Copy", einfach klicken und dann hat man den Token in der zwischenablage
- In der .env Datei muss jetzt einfach "DISCORD_BOT_TOKEN=(hier token vom Developer Portal einfügen)
- Am Ende müssen jetzt noch die IDs getauscht werden damit diese auf dem eingefügten Server passen


IDs die getauscht werden müssen:
welcome.py --> channel_id
leave.py --> channel_id
logs.py --> log_channel_id

Um den Bot nun zu starten einfach python bot.py in der cmd ausführen

-----------------------
English:
To be able to run this bot yourself, you must take the following steps:
- create a new application in the Discord developer portal (https://discord.com/developers/applications) --> https://screens.paccothetaco.com/ScreensX/2024/08/18/Southernhairnosedwombat_rVDbu8adVo.jpg
- if not already installed, install dotenv (pip install python-dotenv)
- in the code, in the same path where bot.py is located, create the file .env
- in the Discord Developer Portal under the item Settings --> Bot, there is a button with ‘Reset Token’, if this was printed you have to verify again that you are really the owner of the account and then you get a token and below it appears the button ‘Copy’, just click and then you have the token in the clipboard
- In the .env file you must now simply enter ‘DISCORD_BOT_TOKEN=(insert token from Developer Portal here)
- At the end, the IDs must now be swapped so that they fit on the inserted server

IDs that need to be swapped:
welcome.py --> channel_id
leave.py --> channel_id
logs.py --> log_channel_id

To start the bot simply execute python bot.py in the cmd