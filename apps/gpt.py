import openai
import sys
import os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir,'..'))
sys.path.append(parent_dir)
from utils.config import *
from utils.logger import *

class ChatGPT:
    def __init__(self):
        self.api_key = read_config()['openai'][0]['openai_key']
        openai.api_key = self.api_key
        self.messages = [{"role": "system", "content": "你现在是很有用的助手！"}]

    def generate_answer(self, prompt):
        self.messages.append({"role": "user", "content": f"{prompt}"})
        completion = openai.ChatCompletion.create(
            model=read_config()['openai'][1]['gpt_model'],
            messages=self.messages,
            temperature=0.7
        )
        res_msg = completion.choices[0].message
        self.messages.append({"role": "assistant", "content": res_msg["content"].strip()})
        return res_msg["content"]
    