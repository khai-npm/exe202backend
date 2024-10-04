# This example requires the 'message_content' intent.
import asyncio
from beanie import init_beanie
from src.models.account import account
from src.models.payment import payment
from src.models.token import token
from src.models.server import server
from src.models.task import task
from src.models.participant import participant 
from email import message
import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from src.events.startup import events as startup_event

bot_token = "MTI0MjE0NTY0NzM4MTk3MDk3NQ.G7jooM.sDG1zPvx0YOPFhsv-7Qg-JX2iOwfGmhHfdi90Y"
async def run_db():
    db_instance = AsyncIOMotorClient("mongodb://localhost:27017/")
    await init_beanie(
        database=db_instance["exe_bot"], document_models=[account, participant, payment,
                                                         server, task, token ]
    )

class MyClient(discord.Client):
    async def on_ready(self):
        await run_db()
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content == "tất cả tại":
            await message.reply('Trương Hải Minh', mention_author=True)





description = "Service exe201 discord bot"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix='?cber ', description=description, intents=intents)

client = MyClient(intents=intents)

@bot.event
async def on_ready():
     await run_db()

     print(" bot server started !")


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def register(ctx):
    try:
        get_server_id = ctx.guild.id
        print(get_server_id)
        get_server_owner = ctx.guild.owner
        print(get_server_owner)
        get_server_name = ctx.guild.name
        print(get_server_name)
        current_server = await server.find_one(server.server_id==str(get_server_id))

        print("check coi co chay qua dong nay khong ?")
        if current_server:
            raise Exception("server alrady registered !")
        new_server_data = server(server_id=str(get_server_id),
                                 server_owner=str(get_server_owner),
                                 tasks=[],
                                 redeem_token="",
                                 server_name=str(get_server_name))
        print (new_server_data) 
        await new_server_data.insert()


        await ctx.send("server : "+ str(get_server_id) + "registered task management service")
    except Exception as e:
        await ctx.send("Error :" + str(e))



@bot.event
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
        await guild.system_channel.send(to_send)


@bot.event
async def on_disconnect():
    print("Bot disconnected")

@bot.event
async def on_resumed():
    print("Bot resumed")

if __name__ == "__main__":
    bot.run(bot_token)
