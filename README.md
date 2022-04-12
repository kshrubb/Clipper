# Clipper v1.1
I format your clips and automatically create a discussion thread for you! Created by kshrubb#5938!

Required Software: You will need Python 3.8 and Py-Cord 2.0.0b7.

Installation:

  On Linux:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.8

    pip install py-cord==2.0.0b7

  On Windows:

    Install the latest Python 3.8.x from their website.

    Then enter in CMD: py -3 -m pip install -U py-cord
    
Initializing Clipper:
1) Edit .env and modify BOT_TOKEN to reflect your bot's token.
2) Execute main.py with python3.8.
3) Invite Clipper to your server.
4) At this point you can open servers.json and remove the entry for the Clipper server if you choose.
5) Pass Clipper an existing channel ID using /set_clips <channel-id> to designate this channel as the clips channel.

Example format for servers.json:
```  
  "<your-server-id>": {
        "name": "<server-name>",
        "CLIPS_CHANNEL_ID": "<clips-channel-id>",
        "RATE_LIMITER": "0"
    }
```

Using Clipper:
1) Use /clipperhelp for an overview of it's commands.
2) To start the bot: python3 main.py
