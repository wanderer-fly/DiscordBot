import os

from discord.ext import commands

from utils.logger import Logger
from utils.logger import Level

# Workspace
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir,'..'))

from apps.gpt import ChatGPT


gpt = ChatGPT()

@commands.command(name="ask")
async def ask(ctx, message):
    await ctx.send(f"ChatGPT Response: {gpt.generate_answer(message)}")

@ask.error
async def ask_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You forgot your question!")
        Logger(Level.WARNING, f"{ctx.message.author} called the API but no question given")