import openai
import logging
import itertools
from utils.fd55_config import Config
config = Config()

class ChatGPT:
    def __init__(self):
        openai.api_key = f"{str(config.get('AI', 'api_key'))}"
        self.engine = "text-davinci-003"

    def send_openai_request(self, prompt):
        try:
            logging.info("Creating request to OpenAI")
            output = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                max_tokens=2048,
                temperature=0,
                stream=True
            )
            logging.info("Recieved answer:")
            print("#################################")
            print("######## OpenAI Response ########")
            print("#################################")
            for event in itertools.islice(output, 1, None):
                event_text = event['choices'][0]['text']
                print(f"{event_text}", end="", flush=True)
            print("\n\n#################################")
        except:
            logging.error("Failed to get a response from OpenAI")
            exit()
