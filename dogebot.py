import discord
import os
import time

class dogebot():
    def __init__(self):
        self.connectedToVC: bool = False
        self.voiceClient: discord.VoiceClient = None
        
    
    #Action Functions
    #----------------
    async def joinVCFromMessage(self, msg: discord.Message) -> None:
        authorVoiceClient = msg.author.voice
        if authorVoiceClient == None or type(authorVoiceClient.channel) != discord.VoiceChannel:
            await msg.channel.send("Join a vc pls")
            return
        
        self.connectedToVC = True
        self.voiceClient = await authorVoiceClient.channel.connect()    
    
    async def leaveVC(self) -> None:
        await self.voiceClient.disconnect()
        self.connectedToVC = False
    
    async def playYTLink(self, msg: discord.Message) -> None:
        if self.connectedToVC:
            youtubeLink = msg.content[5:]
            youtubeName = msg.content[5:].replace("/", "x").replace("#", "x").replace(":", "x").replace("?", "x")
            audioSourcePath = f".\music\{youtubeName}.wav"
            os.system(f".\yt-dlp.exe -q -i --extract-audio --audio-format wav --audio-quality 0 -o {youtubeName} --paths .\music {youtubeLink}")
            while not os.path.isfile(audioSourcePath):
                time.sleep(0.1)
            self.voiceClient.play(discord.FFmpegPCMAudio(audioSourcePath))
    
        
    #On Event Functions
    #------------------
    def handle_user_messages(self, msg: discord.Message) -> tuple[str, bool, discord.Message]:
        print(f"Got Message: {msg.content}")
        print(f"From Author: {msg.author.name}")
        message = msg.content.lower() #Converts all inputs to lower case
        if (msg.author.name == 'retrogarde'):
            return ('I Love you pookie <@459482369275985921>', False, None)
        
        if(len(message) > 3 and message.startswith("play")):
            return ('sir yes sir', True, msg)
        return None
    
    async def processMessage(self, message: discord.Message) -> None:
        try:
            botfeedbackPacket = self.handle_user_messages(message)
            if botfeedbackPacket != None:
                if botfeedbackPacket[1]:
                    await self.joinVCFromMessage(botfeedbackPacket[2])
                    await self.playYTLink(botfeedbackPacket[2])
                else:
                    await message.channel.send(botfeedbackPacket[0])
        except Exception as error:
            print(error)
    
    
    def runBot(self) -> None:
        f = open("discordBotToken.txt", "r")
        discord_token = f.read()
        f.close()
        intents = discord.Intents.all()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print({client.user}, 'is live')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return
            await self.processMessage(message)

        client.run(discord_token)