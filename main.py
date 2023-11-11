import sys

import discord
from discord.ext import commands

from utils.logger import Logger
from utils.logger import Color

from apps.gpt import ChatGPT
from apps.rand import *

from utils.blacklist import Blacklist
from utils.dbhelper import DBHelper

import utils.config

# OpenAI API
gpt = ChatGPT()
# Database Helper
db = DBHelper()
# Blacklist
blacklist = Blacklist(db)

Logger(Color.INFO, f"Discord Module Version: {discord.__version__}")
Logger(Color.INFO, f"Database enabled status: {db.return_db_status()}")

try:
    token = utils.config.read_config()['discord'][0]['discord_token']
    if token:
        Logger(Color.INFO, f"Token: {token}")
    else:
        Logger(Color.ERROR, "Token not found in config, exiting...")
        sys.exit(0)
except:
    Logger(Color.ERROR, "Token not found, exiting...")

# For traditional command option
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix = '/', intents = intents) # Default command prompt

# 报错的代码(discord.commands.core line 386 `raise CheckFailure()`)被解决掉了，不需要handler了
# For slash_command errors
# ExceptionHandler.setup(bot)

# Nov.11, 2023 - 我是小小羊的特别关心！！！
@bot.event
async def on_ready():
    Logger(Color.INFO, f"Bot logged in as {bot.user.name}")

@bot.check
async def check_black_list(ctx):
    user_id = str(ctx.author.id)
    if blacklist.check_user(user_id):
        await ctx.send(f"{ctx.author} You are in blacklist")
        return False # 会抛出discord.ext.commands.errors.CheckFailure，由on_check_failure()捕获
    else:
        return True
    
@bot.event
async def on_command_error(ctx, error):
    #pass
    if isinstance(error, commands.CommandError):
        await ctx.send(f"Command Error: {error}")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"Check Failure: {error}")

def black_list_check():
    async def predicate(ctx):
        user_id = str(ctx.author.id)
        if blacklist.check_user(user_id):
            await ctx.send("You are in blacklist!")
            return False
        return True
    return commands.check(predicate)


@bot.slash_command(name = "hi", description = "Say hello to bot")
async def hello(ctx):
    await ctx.respond("Hey!")

#@permission_check()
@bot.command(name = "test", description = "Test Command")
async def test_cmd(ctx):
    if ctx.author == bot.user:
        return

    await ctx.send(
            f"""
            Author: {ctx.author} ID: {ctx.author.id}\n
            Guild: {ctx.guild} ID: {ctx.guild.id}\n
            Channel: {ctx.channel} ID: {ctx.channel.id}\n
            Message: {ctx.message} \n
            Command Info: {ctx.command}
            """
            )
    await ctx.send(ctx.author.mention)

@bot.command(name="ask")
async def ask(ctx, message):
    await ctx.send(f"ChatGPT Response: {gpt.generate_answer(message)}")

@ask.error
async def ask_error(ctx, error):
    # 缺少参数的时候抛出的错误，就像是巴巴托斯没有了赛西莉亚花一样
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You forget your question!")
        Logger(Color.WARNING, f"{ctx.message.author} called the API but no question given")

@bot.command(name="fuck")
async def fuck(ctx):
    mentions = ctx.message.mentions
    if mentions:
        for i in range(100):
            for user in mentions:
                await ctx.send(user.mention)

@bot.slash_command(name="random")
async def get_random_int(ctx, start: int, end: int, step: int = 1):
    await ctx.respond(gen_a_random_num(start=start, end=end, step=step))
@get_random_int.error
async def get_random_int_error(ctx, error):
    if isinstance(error, ValueError):
        await ctx.respond("An arguement you input is now an integer")

@bot.command(name="black")
async def blacklist_op(ctx, operation):
    if not blacklist.db_helper.db_enabled:
        await ctx.send("Database not enabled")
        return
    mentions = ctx.message.mentions
    if mentions:
        if operation == 'add':
            for user in mentions:
                result = blacklist.add_user(user.id)
                if result:
                    await ctx.send(f"Add {user.mention} to blacklist")
                    Logger(Color.INFO, f"{user.id} is added to blacklist")
                else:
                    await ctx.send(f"Can't add {user.mention} to blacklist")
                    Logger(Color.ERROR, f"Can't add {user.id} to blacklist")
        elif operation == 'del':
            for user in mentions:
                result = blacklist.del_user(user.id)
                if result:
                    await ctx.send(f"Remove {user.mention} from blacklist")
                    Logger(Color.INFO, f"{user.id} is removed to blacklist")
                else:
                    await ctx.send(f"Can't add {user.mention} to blacklist")
                    Logger(Color.ERROR, f"Can't add {user.id} to blacklist")
        elif operation == 'check':
            for user in mentions:
                result = blacklist.check_user(user.id)
                if result:
                    await ctx.send(f"{user.mention} is in blacklist")
                else:
                    await ctx.send(f"{user.mention} isn't in blacklist")
        else:
            await ctx.send("Invalid operation. Use 'add' or 'del'")
    else:
        await ctx.send("No user mentioned")


bot.run(token)
