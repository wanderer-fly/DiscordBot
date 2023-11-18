import discord
from discord.ext import commands

from utils.logger import Logger, Level

from utils.blacklist import Blacklist
from utils.dbhelper import DBHelper
from utils.permission import Permission

import utils.config # 用不到，下次再用不到就去掉……
import utils

from commands.askgpt import *
from commands.gen_random_int import *

class DcBot:
    def __init__(self, token, db = None):
        # Bot owner id and discord token
        self.owner_id = utils.config.Config().read_config()['bot'][0]['owner_id']
        self.token = token
        self.debug = utils.config.Config().read_config()['bot'][1]['debug']

        # Database Helper
        self.db = utils.db

        # Blacklist
        self.blacklist = Blacklist(self.db)

        Logger(Level.INFO, f"Discord Module Version: {discord.__version__}")
        Logger(Level.INFO, f"Database enabled status: {self.db.return_db_status()}")
        Logger(Level.DEBUG, f"Debug mode: {self.debug}")

        # For traditional command option
        intents = discord.Intents.all()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='/', intents=intents)  # Default command prompt

        # Nov.11, 2023 - 我是小小羊的特别关心！！！
        @self.bot.event
        async def on_ready():
            Logger(Level.INFO, f"Bot logged in as {self.bot.user.name}")

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
                if self.debug:
                    Logger(Level.DEBUG, f"Command Error: {error}")
            elif isinstance(error, commands.CheckFailure):
                await ctx.send(f"Check Failure: {error}")
                if self.debug:
                    Logger(Level.DEBUG, f"Check Failure: {error}")
            elif isinstance(error, discord.errors.CheckFailure): # 不管用
                await ctx.send(f"Check Failure: {error}")
                if self.debug:
                    Logger(Level.DEBUG, f"Check Failure: {error}")

        def is_owner(): # for owner commands like black etc.
            async def predicate(ctx):
                if self.owner_id:
                    return ctx.author.id == self.owner_id
                return True # return True to allow command execute if own_id not enabled
            return commands.check(predicate)
        
        def black_list_check():
            async def predicate(ctx):
                user_id = str(ctx.author.id)
                if self.blacklist.check_user(user_id):
                    await ctx.send("You are in blacklist!")
                    return False
                return True
            return commands.check(predicate)
        
        @self.bot.check
        def permission_check(value):
            async def predicate(ctx):
                if not self.db.db_enabled:
                    return False
                if ctx.guild is None:
                    user_id = str(ctx.author.id)
                    if Permission.get_permission_value(user_id) >= value:
                        return True
                else:
                    return False
            return commands.check(predicate)
        

        @self.bot.slash_command(name="hi", description="Say hello to bot")
        @permission_check(5)
        async def hello(ctx):
            await ctx.respond("Hey!")

        @self.bot.command(name="black")
        @is_owner() # Only owner can run!!!
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
                            Logger(Level.INFO, f"{user.id} is added to blacklist")
                        else:
                            await ctx.send(f"Can't add {user.mention} to blacklist")
                            Logger(Level.ERROR, f"Can't add {user.id} to blacklist")
                elif operation == 'del':
                    for user in mentions:
                        result = self.blacklist.del_user(user.id)
                        if result:
                            await ctx.send(f"Remove {user.mention} from blacklist")
                            Logger(Level.INFO, f"{user.id} is removed from blacklist")
                        else:
                            await ctx.send(f"Can't remove {user.mention} from blacklist")
                            Logger(Level.ERROR, f"Can't remove {user.id} from blacklist")
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
