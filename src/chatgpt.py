"""

"""

import ast
import json
import os
from dotenv import load_dotenv
import openai

class ChatGPT:
    def __init__(self) -> None:
        self.GPT_MODEL = "gpt-3.5-turbo"
        self._load_api_key()

    def _load_api_key(self) -> None:
        load_dotenv('./src/keys.env')
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def chatGPT_conversation(self, pair, parameters) -> None:
        with open('./src/pairs_trading_prompt.json') as fp:
            prompt = json.load(fp)
        
        # prompt['content'] = parameters
        messages = [{ "role": "user", "content": f'{prompt} {parameters}' }]

        response = openai.ChatCompletion.create(model=self.GPT_MODEL, messages=messages)

        content = response.choices[0].message["content"].replace('\"', '\\"').replace('\\n', '\\""').replace('\\\\"', '\\"')
        data = json.loads(content)
            
        with open(f'./res/data/pairs/{pair}.json', 'w', encoding='utf-8') as f:
            ast.literal_eval(json.dump(data, f, ensure_ascii=False, indent=4))

        print(response)

        api_usage = response['usage']
        print("\n\nCURRENT API USAGE\n\n", api_usage)