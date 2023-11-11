import discord
from discord.ext import commands

from utils.logger import Logger, Color

from utils.blacklist import Blacklist
from utils.dbhelper import DBHelper

import utils.config # 用不到，下次再用不到就去掉……

from commands.askgpt import *
from commands.gen_random_int import *

class DcBot:
    def __init__(self, token):
        self.token = token
        # Database Helper
        self.db = DBHelper()
        # Blacklist
        self.blacklist = Blacklist(self.db)

        Logger(Color.INFO, f"Discord Module Version: {discord.__version__}")
        Logger(Color.INFO, f"Database enabled status: {self.db.return_db_status()}")

        # For traditional command option
        intents = discord.Intents.all()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='/', intents=intents)  # Default command prompt

        # Nov.11, 2023 - 我是小小羊的特别关心！！！
        @self.bot.event
        async def on_ready():
            Logger(Color.INFO, f"Bot logged in as {self.bot.user.name}")

        @self.bot.check
        async def check_black_list(ctx):
            user_id = str(ctx.author.id)
            if self.blacklist.check_user(user_id):
                await ctx.send(f"{ctx.author} You are in blacklist")
                return False  # 会抛出discord.ext.commands.errors.CheckFailure，由on_check_failure()捕获
            else:
                return True

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandError):
                await ctx.send(f"Command Error: {error}")
            elif isinstance(error, commands.CheckFailure):
                await ctx.send(f"Check Failure: {error}")

        def black_list_check():
            async def predicate(ctx):
                user_id = str(ctx.author.id)
                if self.blacklist.check_user(user_id):
                    await ctx.send("You are in blacklist!")
                    return False
                return True

            return commands.check(predicate)
        
        # Build in commands

        @self.bot.slash_command(name="hi", description="Say hello to bot")
        async def hello(ctx):
            await ctx.respond("Hey!")

        @self.bot.command(name="black")
        async def blacklist_op(ctx, operation):
            if not self.blacklist.db_helper.db_enabled:
                await ctx.send("Database not enabled")
                return
            mentions = ctx.message.mentions
            if mentions:
                if operation == 'add':
                    for user in mentions:
                        result = self.blacklist.add_user(user.id)
                        if result:
                            await ctx.send(f"Add {user.mention} to blacklist")
                            Logger(Color.INFO, f"{user.id} is added to blacklist")
                        else:
                            await ctx.send(f"Can't add {user.mention} to blacklist")
                            Logger(Color.ERROR, f"Can't add {user.id} to blacklist")
                elif operation == 'del':
                    for user in mentions:
                        result = self.blacklist.del_user(user.id)
                        if result:
                            await ctx.send(f"Remove {user.mention} from blacklist")
                            Logger(Color.INFO, f"{user.id} is removed from blacklist")
                        else:
                            await ctx.send(f"Can't remove {user.mention} from blacklist")
                            Logger(Color.ERROR, f"Can't remove {user.id} from blacklist")
                elif operation == 'check':
                    for user in mentions:
                        result = self.blacklist.check_user(user.id)
                        if result:
                            await ctx.send(f"{user.mention} is in blacklist")
                        else:
                            await ctx.send(f"{user.mention} isn't in blacklist")
                else:
                    await ctx.send("Invalid operation. Use 'add', 'del', or 'check'")
            else:
                await ctx.send("No user mentioned")

    def run(self):
        self.bot.run(self.token)

    def setup(self):
        # Add custom commands here

        # OpenAI API
        self.bot.add_command(ask)
        
        # Random number
        self.bot.add_command(get_random_int)
        self.bot.load_extensions()