import os
import random

from discord.ext import commands

@commands.command(name="random")
async def get_random_int(ctx, start: int, end: int, step: int = 1):
    await ctx.send(random.randrange(start, end, step))

@get_random_int.error
async def get_random_int_error(ctx, error):
    if isinstance(error, ValueError):
        await ctx.send("An argument you input is not an integer")