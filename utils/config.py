import os
import sys

import yaml

class Config:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yaml')
        try:
            with open(self.config_path, 'r') as config_file:
                self.config = yaml.load(config_file, Loader = yaml.FullLoader)
        except:
            print(f"\033[91m config not found, generating a new one... \033[0m")
            self.gen_config()
            sys.exit(1)

    def read_config(self):    
        return self.config

    def gen_config(self):
        data = {
            'discord': [
                {'discord_token': None}
            ],
            'bot': [
                {'owner_id': None},
                {'debug': False}
            ],
            'openai': [
                {'openai_key': None},
                {'gpt_model': 'gpt-3.5-turbo'}
            ],
            'database': [
                {'db_enabled': True},
                {'db_name': 'database.db'}
            ],
            'blacklist': [
                {'blacklist_enabled': True},
                {'blacklist_db': 'database.db'}
            ]
        }
        
        with open(self.config_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)