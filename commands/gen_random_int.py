import os
import random

from discord.ext import commands

# 小辉猫的对象不理他了，小辉猫在伤心w

"""
别人线下认识的推友 -> 互相关注
我线下认识的推友（？ -> 互相拉黑
这里说的是Thanatos星宇
（（（话说有个人叫Thanatos
"""

@commands.command(name="random")
async def get_random_int(ctx, start: int, end: int, step: int = 1):
    await ctx.send(random.randrange(start, end, step))

@get_random_int.error
async def get_random_int_error(ctx, error):
    if isinstance(error, ValueError):
        await ctx.send("An argument you input is not an integer")