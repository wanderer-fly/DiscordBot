import sys

import discord
from discord.ext import commands

from utils.logger import Logger
from utils.logger import Color

from apps.gpt import ChatGPT

import utils.config

gpt = ChatGPT()

try:
    token = utils.config.read_config()['discord'][0]['discord_token']
    if token:
        Logger(Color.INFO, f"Token: {token}").output()
    else:
        Logger(Color.ERROR, "Token not found in config, exiting...").output()
        sys.exit(0)
except:
    Logger(Color.ERROR, "Token not found, exiting...").output()

# If you need proxy for Chinese servers, just add `proxy=""`
#bot = discord.Bot(intents = discord.Intents.all())
bot = commands.Bot(command_prefix = '/')

@bot.event
async def on_ready():
    Logger(Color.INFO, f"Bot logged in as {bot.user.name}").output()

@bot.slash_command(name = "hi", description = "Say hello to bot")
async def hello(ctx):
    await ctx.respond("Hey!")

@bot.slash_command(name = "test", description = "Test Command")
async def test_cmd(ctx):
    if ctx.author == bot.user:
        return

    await ctx.respond(
            f"""
            AUthor: {ctx.author} ID: {ctx.author.id}\n
            Guild: {ctx.guild} ID: {ctx.guild.id}\n
            Channel: {ctx.channel} ID: {ctx.channel.id}\n
            Message: {ctx.message} \n
            Command Info: {ctx.command}
            """
            )
    await ctx.send(ctx.author.mention)

@bot.slash_command(name="ask", description="Ask ChatGPT")
async def ask(ctx, message):
    await ctx.send(f"ChatGPT Response: {gpt.generate_answer(message)}")


bot.run(token)
