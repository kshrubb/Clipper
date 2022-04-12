# Clipper v1.1
I format your clips and automatically create a discussion thread for you! Created by kshrubb#5938!

Required Software: You will need Python 3.8, Python-DotEnv and Py-Cord 2.0.0b7.

Installation:

  On Linux:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.8

    python3.8 pip install python-dotenv
    python3.8 pip install py-cord==2.0.0b7

  On Windows:

    Install the latest Python 3.8.x from their website.

    py -3 -m pip install python-dotenv
    py -3 -m pip install -U py-cord==2.0.0b7
    
Initializing Clipper:
1) Run with: python3.8 main.py
2) Edit .env and modify BOT_TOKEN to reflect your bot's token.
3) Run the bot again
4) Invite Clipper to your server.
5) Pass Clipper an existing channel ID using /set_clips <channel-id> to designate this channel as the clips channel.

Using Clipper:
1) To start the bot: python3.8 main.py
2) Use /clipperhelp for an overview of it's commands.
