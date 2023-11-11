import sys
from dcbot import DcBot

from utils.logger import Logger
from utils.logger import Color

import utils.config

if __name__ == '__main__':
    """
    这是一个故事，关于一个超可爱、超善良的小男孩
    你帽写代码无聊就会写一点注释，，，没什么
    话说这个pyyaml好难用
    """
    try:
        token = utils.config.read_config()['discord'][0]['discord_token']
        if token:
            Logger(Color.INFO, f"Token: {token}")
        else:
            Logger(Color.ERROR, "Token not found in config, exiting...")
            sys.exit(0)
        # 傻逼bot不写下面就会把所有异常当作Token not found（虽然有其他办法但是懒得了。。。
        bot = DcBot(token=token)
        bot.setup()
        bot.run()
    except Exception as e:
        # 林深时候见鹿，溪午不闻钟 ————李白
        # 重构代码很无聊的awa
        Logger(Color.ERROR, f"Bot start failed: {e}")
    