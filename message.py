import os
import sys

# import dotenv
import httpx


class Config:
    def __init__(self, telegram_token, telegram_chat_id, rocket_chat_url, rocket_chat_token, rocket_chat_user_id, rocket_chat_channel, message_text, enable_telegram = 'false', enable_rocket_chat = 'false'):
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.rocket_chat_url = rocket_chat_url
        self.rocket_chat_token = rocket_chat_token
        self.rocket_chat_user_id = rocket_chat_user_id
        self.rocket_chat_channel = rocket_chat_channel
        self.message_text = message_text
        self.enable_telegram = enable_telegram
        self.enable_rocket_chat = enable_rocket_chat

    # print
    def __str__(self):
        return f'Config(telegram_token={self.telegram_token}, telegram_chat_id={self.telegram_chat_id}, rocket_chat_url={self.rocket_chat_url}, rocket_chat_token={self.rocket_chat_token}, rocket_chat_user_id={self.rocket_chat_user_id}, rocket_chat_channel={self.rocket_chat_channel}, message_text={self.message_text}, enable_telegram={self.enable_telegram}, enable_rocket_chat={self.enable_rocket_chat})'

def get_vars() -> Config:
    # dotenv.load_dotenv()
    # print(os.environ)
    return Config(
        telegram_token = os.environ['INPUT_TELEGRAM_TOKEN'],
        telegram_chat_id = os.environ['INPUT_TELEGRAM_TO'],
        rocket_chat_url = os.environ['INPUT_ROCKET_CHAT_URL'],
        rocket_chat_token = os.environ['INPUT_ROCKET_CHAT_TOKEN'],
        rocket_chat_user_id = os.environ['INPUT_ROCKET_CHAT_USERID'],
        rocket_chat_channel = os.environ['INPUT_ROCKET_CHAT_TARGET_CHAT'],
        message_text = os.environ['INPUT_MESSAGE_TEXT'],
        enable_rocket_chat = os.environ['INPUT_ROCKET_CHAT'],
        enable_telegram = os.environ['INPUT_TELEGRAM'],
    )

def send_telegram_message(config: Config):
    print(config)
    assert config.enable_telegram == 'true' and config.telegram_token and config.telegram_chat_id and config.message_text
    url = f'https://api.telegram.org/bot{config.telegram_token}/sendMessage'
    text = config.message_text.replace("\\n", "\n")
    data = {
        'chat_id': config.telegram_chat_id,
        'text': text,
        'parse_mode': 'markdown'
    }
    response = httpx.post(url, json=data)
    if response.status_code != 200:
        print(f'Error while posting message to Telegram \n{response.content}')
        print(response.text)
        sys.exit(1)

def send_rocket_chat_message(config: Config):
    assert config.enable_rocket_chat == 'true' and config.rocket_chat_url and config.rocket_chat_token and config.rocket_chat_user_id and config.rocket_chat_channel and config.message_text
    url = f'{config.rocket_chat_url}/api/v1/chat.postMessage'
    headers = {
        'X-Auth-Token': config.rocket_chat_token,
        'X-User-Id': config.rocket_chat_user_id,
        'Content-type': 'application/json'
    }
    text = config.message_text.replace("\\n", "\n")
    data = {
        'channel': config.rocket_chat_channel,
        'text': text,
        'alias': 'Beep Boop',
        'avatar': 'https://img.freepik.com/premium-vector/cute-robot-waving-hand-cartoon-illustration_138676-2744.jpg?w=2000'
    }
    response = httpx.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f'Error while posting message to Rocket.Chat \n{response.content}')
        print(response.text)
        print(f'URL: {url}')
        print(f'Headers: {headers}')
        print(f'Data: {data}')
        print(f'Response headers: {response.headers}')
        sys.exit(1)

def main():
    config = get_vars()
    if config.enable_telegram == 'true':
        send_telegram_message(config)
    if config.enable_rocket_chat == 'true':
        send_rocket_chat_message(config)

if __name__ == '__main__':
    main()
    print('Message sent successfully!')