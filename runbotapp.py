# This example requires the 'message_content' intent.
import os
import asyncio
from prettytable import PrettyTable
import datetime
from tabulate import tabulate
from beanie import init_beanie
from schemas_for_bot.task_list_schema import task_list_schema
from src.models.account import account
from src.models.payment import payment
from src.models.token import token
from src.models.server import server
from src.models.task import task as task_list
from src.models.participant import participant 
from email import message
import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from src.events.startup import events as startup_event
from dotenv import load_dotenv
from bson import ObjectId
from googletrans import Translator

load_dotenv()


bot_token = os.getenv("BOT_TOKEN")
connection_string = os.getenv("CONNECTION_STRING")


async def run_db():
    print("running db connection : " + connection_string)
    db_instance = AsyncIOMotorClient(connection_string)
    await init_beanie(
        database=db_instance["exe_bot"], document_models=[account, participant, payment,
                                                         server, task_list, token ]
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
        await ctx.send(str(e))

@bot.command()
async def task(ctx, command : str, * , data : str = None):
    try:
        get_server_id = ctx.guild.id
        current_server = await server.find_one(server.server_id==str(get_server_id))
        if not current_server:
            raise Exception("server must be registerd to use this feature ! use '?cber help' for more infomation")

        match command:
            case "list":
                true_result : list[task_list_schema] = []
                new_true_result_data = task_list_schema(task_id="", task_title="")
                result : list[task_list] = []
                all_task =await task_list.find_many(task_list.server_id == str(ctx.guild.id)).to_list()

                # for i in all_task:
                #     new_true_result_data.task_id = str(i.id)
                #     new_true_result_data.task_title = str(i.task_title)
                #     true_result.append(new_true_result_data)


                # sort_result = [[str(i.id), str(i.task_title)] for i in all_task]

                # if not all_task: 
                #     raise Exception("not any task to show !")

                # header = ["id", "title"]
                # table = tabulate(sort_result, header, tablefmt="github", stralign="center", numalign="center")


                # final_result = "\n".join([str(obj) for obj in true_result])
                # print(final_result)

                table = PrettyTable()
                table.field_names = ["id", "title"]
                
                for i in all_task:
                    table.add_row([str(i.id), str(i.task_title)])


                table_str = f"```\n{table}\n```"

                await ctx.send(table_str)

            case "add":
                if not data:
                    raise Exception("command 'add' requrie new task's title")
                

                try:
                    get_server_id = ctx.guild.id
                    current_server = await server.find_one(server.server_id==str(get_server_id))
                    if not current_server:
                        raise Exception("server must be registerd to use this feature ! use '?cber help' for more infomation")
                    author = ctx.author
                    new_task = task_list(task_title=data,
                             server_id=str(get_server_id),
                             add_by=str(author.name),
                             task_desc="",
                             end_date=datetime.datetime.now(),
                             start_date=datetime.datetime.now(),
                             participants=[],
                             success=False)
        
                    await new_task.insert()
                    current_server.tasks.append(str(new_task.id))
                    await current_server.save()
                    await ctx.send("task :" + data + " added successfully !")

        

        
        

                except Exception as e:
                    # raise Exception(str(e))
                    await ctx.send(str(e))
            case "get":
                get_task = await task_list.find_one(task_list.id == ObjectId(data))
                if not get_task:
                    raise Exception("'?cber task get <task_id>'. to see task id, view "+
                                    "from command '?cber task list'")
                
                for i in get_task.participants:
                    if ctx.author.name == i:
                        raise Exception("you are already signed for this task")
                
                get_task.participants.append(str(ctx.author.name))
                await get_task.save()

                await ctx.send(f"[{ctx.author.name}] accepted task {str(get_task.id)} with title |[{get_task.task_title}]|")
                

            case "detail":
                get_task = await task_list.find_one(task_list.id == ObjectId(data))
                if not get_task:
                    raise Exception("'?cber task detail <task_id>'. to see task id, view"+
                                    " from command '?cber task list'")
                await ctx.send(f"[{ctx.author.name}] accepted task {str(get_task.id)} with title |[{get_task.task_title}]|")

            case _:
                raise Exception("command not found !")
    except Exception as e:
        await ctx.send(str(e))




# @bot.command()
# async def task_add(ctx, * , data : str):
#     try:
#         get_server_id = ctx.guild.id
#         current_server = await server.find_one(server.server_id==str(get_server_id))
#         if not current_server:
#             raise Exception("server must be registerd to use this feature ! use '?cber help' for more infomation")
#         author = ctx.author
#         new_task = task_list(task_title=data,
#                              server_id=str(get_server_id),
#                              add_by=str(author.name),
#                              task_desc="",
#                              end_date=datetime.datetime.now(),
#                              start_date=datetime.datetime.now(),
#                              participants=[],
#                              success=False)
        
#         await new_task.insert()
#         current_server.tasks.append(str(new_task.id))
#         await current_server.save()
#         await ctx.send("task :" + data + " added successfully !")

        

        
        

    # except Exception as e:
    #     # raise Exception(str(e))
    #     await ctx.send(str(e))

@bot.command()
async def clear_msg(ctx, amount: int):
    try:
        if ctx.guild.owner is not ctx.author:
            raise Exception("only owner can use this feature !")
        
        await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message itself
        await ctx.send("["+str(ctx.author.name) + "] deleted " + str(amount) + " messages !")
    except Exception as e:
        await ctx.send(str(e))

@bot.command()
async def trans(ctx, lang : str, * , data = None):
    try:
        if data is None:
            raise Exception("no data to translate")
        match lang:
            case "vi":
                print(str(data))

                translator = Translator()
                detection = translator.detect(str(data))
                result = translator.translate(str(data), dest='vi')

                msg = f"```Language Detected : {detection.lang}\n\n -> {result.text}  ```"
                await ctx.send(msg)


            case "en":
                print(str(data))

                translator = Translator()
                detection = translator.detect(str(data))
                result = translator.translate(str(data), dest='en')

                msg = f"```Language Detected : {detection.lang}\n\n -> {result.text}  ```"
                await ctx.send(msg)
            case _:
                await ctx.send("supportted language:\nvi - Tiếng Việt\nen - English")

    except Exception as e:
        raise Exception(e)
        # await ctx.send(str(e))
        

    


@bot.event
async def on_member_join(member):
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
