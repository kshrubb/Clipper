# Clipper
I format your clips and automatically create a discussion thread for you! Created by kshrubb#5938!

Required Software
  You will need Python 3.8 and Py-Cord 2.0.0b7.

  On Linux:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.8

    pip install py-cord==2.0.0b7

  On Windows:

    Install the latest Python 3.8.x from their website.

    Then enter in CMD: py -3 -m pip install -U py-cord
    
Initializing Clipper
  Edit .env and modify BOT_TOKEN to reflect your bot's token.
  Execute main.py with python3.8.
  Invite Clipper to your server.
  Pass Clipper an existing channel ID using /set_clips <channel-id> to designate this channel as the clips channel.
 
Using Clipper
  Use /clipperhelp for an overview of it's commands.
  
  To start the bot: python3 main.py
