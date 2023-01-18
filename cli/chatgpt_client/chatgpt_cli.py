import openai
import logging
import itertools
from utils.fd55_config import Config
config = Config()


class ChatGPT:
    def __init__(self):
        openai.api_key = f"{str(config.get('AI', 'api_key'))}"
        self.engine = "text-davinci-003"

    def send_openai_request(self, prompt, full_output=False, file=None, iterations=None):
        try:
            logging.info("Creating request to OpenAI")
            if file is not None:
                logging.info(f"Manifesting prompt with file '{file}'")
                with open(file, 'r') as f:
                    file_content = f.read()
                    prompt += '. File to modify: \n' + file_content
                    logging.debug(f"Manifested new prompt:\n{prompt}")
            stream = False if full_output else True
            output = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                max_tokens=2048,
                temperature=0.5,
                stream=stream
            )
            if full_output is not False:
                logging.info("Waiting for full output generation")
                full_output = output.choices[0].text
                print(full_output[1::])
                logging.info("Finished generation")
            else:
                logging.info("Recieved answer:")
                print("#################################")
                print("######## OpenAI Response ########")
                print("#################################\n")
                for event in itertools.islice(output, 1, None):
                    event_text = event['choices'][0]['text']
                    print(f"{event_text}", end="", flush=True)
                print("\n\n#################################")
        except BaseException:
            logging.error("Failed to get a response from OpenAI")
            exit()

