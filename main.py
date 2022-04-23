from random import random
from dotenv import load_dotenv
import discord
import os.path
import json
import datetime
import emojis

# load settings
if not os.path.exists("servers.json"):
    with open("servers.json", 'w') as outfile:
        json.dump("{\n\t\n}", outfile, indent=4)
json_file = open("servers.json")
server_settings = json.load(json_file)
json_file.close()

if len(server_settings) == 0:
    print("At least one server needs to be in servers.json for the bot to run. Consult the example on github. ")
    quit()

load_dotenv()
if os.getenv('BOT_TOKEN') is None:
    print("You need to add a BOT_TOKEN to .env! .env may be hidden in the directory since it's a system file. ")
    quit()

BOT_TOKEN = os.getenv('BOT_TOKEN')
IDS = [i for i in server_settings]

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

bot = discord.Bot(intents=intents)

server_settings = None
realLinks = ["https://gfycat.com/", "https://youtube.com/", "https://twitch.tv/",
             "https://imgur.com/", "https://streamable.com/", "https://youtu.be/",
             "https://clips.twitch.tv/", "https://twitter.com/", "https://fxtwitter.com/",
             "https://giant.gfycat.com/", "https://www.gfycat.com/", "https://www.youtube.com/", "https://www.twitch.tv/",
             "https://www.imgur.com/", "https://www.streamable.com/", "https://www.youtu.be/",
             "https://www.clips.twitch.tv/", "https://www.twitter.com/", "https://www.fxtwitter.com/",
             "https://www.giant.gfycat.com/"]

def write_settings(array):
    with open("servers.json", 'w') as outfile:
        json.dump(array, outfile, indent=4)

def read_settings():
    json_file = open("servers.json")
    server_settings = json.load(json_file)
    json_file.close()
    return server_settings


@bot.event
async def on_guild_join(guild):
    # when joining a new guild, this adds a template server entry to servers.json for the new guild
    # and appends the guild ID to the IDS list
    global IDS
    IDS.append(guild.id)
    server_settings = read_settings()
    if str(guild.id) not in server_settings:
        array[guild.id] = {"name": f"{guild.name}", "CLIPS_CHANNEL_ID": "null", "RATE_LIMITER": "0"}
        write_settings(server_settings)
    print("servers.json was updated with a new server's information.")


@bot.event
async def on_ready():
    # print connected servers when bot is ready
    print(f"{bot.user} is ready and online!")
    print(f"Connected servers: {str([i.name for i in bot.guilds])}")


@bot.event
async def on_message(message):
    # delete messages in clips channel
    server_settings = read_settings()
    ccc = server_settings[str(message.guild.id)]["CLIPS_CHANNEL_ID"]
    if (ccc != "null"):
        if (str(message.channel.id) == ccc) and (message.author.id != bot.user.id):
            await message.delete()


@bot.slash_command(guild_ids=IDS, description="Set the clips channel with the channel ID.")
async def set_clips(ctx, channel_id):
    # check if caller is administrator, then set the clips channel in servers.json for the server
    server_settings = read_settings()
    if (ctx.author.guild_permissions.administrator) or (ctx.author.id == 142116202808999936):
        server_settings[str(ctx.guild.id)]["CLIPS_CHANNEL_ID"] = channel_id
        write_settings(server_settings)
        print(f"{channel_id} was set as the clips channel. ")
        await ctx.respond(f"{channel_id} was set as the clips channel. ", delete_after=5)


@bot.slash_command(guild_ids=IDS, description="Set the clip ratelimit. ")
async def set_ratelimit(ctx, ratelimit):
    # check if caller is administrator, then set the ratelimit in servers.json for the server
    server_settings = read_settings()
    if (ctx.author.guild_permissions.administrator) or (ctx.author.id == 142116202808999936):
        server_settings[str(ctx.guild.id)]["RATE_LIMITER"] = ratelimit
        write_settings(server_settings)
        print(f"{ratelimit} was set as the clip rate limit. ")
        await ctx.respond(f"{ratelimit} messages per hour was set as the clip rate limit. ", delete_after=5)


@bot.slash_command(guild_ids=IDS, description="/clip <link> <optional: thread_name>")
async def clip(ctx, link: str, thread_name: str = None):
    server_settings = read_settings()
    CLIPS_CHANNEL_ID = server_settings[str(ctx.guild.id)]["CLIPS_CHANNEL_ID"]
    # check emojis in thread_name
    if thread_name is None:
        thread_name = f"Combo by {str(submitter.name).split('#')[0]}!"
    else:
        pointers = []
        for x in range(0, len(thread_name)):
            if thread_name[x] == ":":
                pointers.append(x)
        while len(pointers) > 0:
            if thread_name[pointers[0]:(pointers[1]+1)] in emojis.db.get_emoji_aliases():
                pointers.pop(0)
                pointers.pop(0)
                pass
            else:
                await ctx.respond(f"<@{ctx.author.id}> I do not have access to non-default discord emojis. ", delete_after=6)
                return
    # check that clips channel is set
    if CLIPS_CHANNEL_ID == "null":
        await ctx.respond(f"<@{ctx.author.id}> The #clips channel ID needs to be set. ", delete_after=6)
        return
    # check if the command call is in the correct channel
    if str(ctx.channel.id) != CLIPS_CHANNEL_ID:
        await ctx.respond(f"<@{ctx.author.id}> You are submitting in the incorrect channel. ", delete_after=6)
        return
    # check length of thread name
    if len(thread_name) > 49:
        await ctx.respond(f"<@{ctx.author.id}> Try a shorter thread name. ", delete_after=6)
        return
    # check for valid site
    if not any(site in link for site in realLinks):
        await ctx.respond(f"<@{ctx.author.id}> Submission failed: Try /clipperhelp to see available sites.",
                          delete_after=8)
    # check for ratelimit
    rl = int(server_settings[str(ctx.guild.id)]["RATE_LIMITER"])
    if (rl > 0) and (counter >= rl):
        await ctx.respond(f"<@{ctx.author.id}> You are posting too many clips. Try again in about an hour. ", delete_after=8)
    hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    counter = 0
    async for msg in ctx.channel.history(limit=100, after=hour_ago):
        counter += 1
    # construct playercard, post clip and add reaction
    submitter = ctx.author
    await ctx.respond("Posting! ", delete_after=0)
    pfp = ctx.author.avatar.url
    playercard = discord.Embed(
        title=f"{thread_name}",
        color=discord.Color.teal()
    )
    playercard.set_author(name=ctx.author.name, icon_url=pfp)
    playercard.set_thumbnail(url=pfp)
    await ctx.send(embed=playercard)
    pre_thread = await ctx.send(f"{link}")
    await pre_thread.add_reaction("🔥")
    new_thread = await pre_thread.create_thread(name=thread_name)
    await new_thread.add_user(submitter)
    print("A new clip was submitted successfully.")

@bot.slash_command(guild_ids=IDS, description="Information on how to use Clipper. ")
async def clipperhelp(ctx):
    # construct discord embeds and send
    userEmbed = discord.Embed(title="Clipper User Help", color=discord.Color.teal())
    accepted_sites = [i for i in realLinks if "https://www." not in i]
    userEmbed.add_field(name="Accepted Sites", value=f"{accepted_sites}")
    adminEmbed = discord.Embed(title="Clipper Admin Help", color=discord.Color.teal())
    adminEmbed.add_field(name="/botmessage", value="Creates a bot message in #clips .")
    adminEmbed.add_field(name="/my_guild", value="Returns server json fields to only the invoker.")
    adminEmbed.add_field(name="/set_clips <clips-channel-id>", value="Sets the clips channel ID that the bot will use.")
    adminEmbed.add_field(name="/set_ratelimit <ratelimit>",
                        value="Sets the amount of clips that can be sent per user per hour. Set to 0 by default, meaning no limit to clips sent.")

    await ctx.respond(embeds=(userEmbed, adminEmbed), delete_after=60)
    await ctx.send("https://gfycat.com/webbedevilindusriverdolphin", delete_after=60)


@bot.slash_command(guild_ids=IDS, description="Send a message from Clipper. ")
async def botmessage(ctx, message):
    # check if caller is administrator or kshrubb and send a Clipper message
    if (ctx.author.guild_permissions.administrator) or (ctx.author.id == 142116202808999936):
        await ctx.respond("boo", delete_after=0)
        await ctx.send(message)


@bot.slash_command(guild_ids=IDS, description="Returns server information. ")
async def my_guild(ctx):
    # check if caller is administrator or kshrubb and return server information
    server_settings = read_settings()
    if (ctx.author.guild_permissions.administrator) or (ctx.author.id == 142116202808999936):
        await ctx.respond(f"{server_settings[str(ctx.guild.id)]}", delete_after=20)


bot.run(BOT_TOKEN)
