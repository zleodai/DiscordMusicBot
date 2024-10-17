import discord
import os
import time

connectedToVC = False
voiceClient: discord.VoiceClient = None

def handle_user_messages(msg: discord.Message) -> tuple[str, bool, discord.Message]:
    print(f"Got Message: {msg.content}")
    print(f"From Author: {msg.author.name}")
    message = msg.content.lower() #Converts all inputs to lower case
    if (msg.author.name == 'retrogarde'):
        return ('I Love you pookie <@459482369275985921>', False, None)
    
    if(len(message) > 3 and message[:4] == 'play'):
        return ('sir yes sir', True, msg)
    return None

async def joinVCFromMessage(msg: discord.Message) -> discord.VoiceClient:
    voiceChannel = msg.author.voice
    if voiceChannel == None:
        await msg.channel.send("Join a vc pls")
        return
    voiceChannel = voiceChannel.channel
    if type(voiceChannel) != discord.VoiceChannel:
        await msg.channel.send("Join a vc rn")
        return
    
    connectedToVC = True
    return await voiceChannel.connect()

async def playMusic(msg: discord.Message):
    if not connectedToVC:
        voiceClient = await joinVCFromMessage(msg)
        if voiceClient != None:
            await msg.channel.send(f"joined {voiceClient.channel.name}")
    
    youtubeLink = msg.content[5:]
    youtubeName = msg.content[5:].replace("/", "x").replace("#", "x").replace(":", "x").replace("?", "x")
    audioSourcePath = f".\music\{youtubeName}.wav"
    os.system(f".\yt-dlp.exe -q -i --extract-audio --audio-format wav --audio-quality 0 -o {youtubeName} --paths .\music {youtubeLink}")
    while not os.path.isfile(audioSourcePath):
        time.sleep(0.1)
    await msg.channel.send(f"Downloaded {youtubeName}")
    voiceClient.play(discord.FFmpegPCMAudio(audioSourcePath))
    
async def processMessage(message: discord.Message):
    try:
        botfeedbackPacket = handle_user_messages(message)
        if botfeedbackPacket != None:
            if botfeedbackPacket[1]:
                await playMusic(botfeedbackPacket[2])
            else:
                await message.channel.send(botfeedbackPacket[0])
    except Exception as error:
        print(error)

def runBot():
    discord_token = 'MTI5NjI5MzkxMjUxNTk3MzEzMA.Gz2UbQ.OaKrpbIuBXBTvEsM3PIfWhVODNepXj4egTK8uI'
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print({client.user}, 'is live')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message)

    client.run(discord_token)