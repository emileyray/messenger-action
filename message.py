import os
import sys

# import dotenv
import httpx


class Config:
    def __init__(self, telegram_token, telegram_chat_id, rocket_chat_url, rocket_chat_token, rocket_chat_user_id, rocket_chat_channel, message_text, enable_telegram = True, enable_rocket_chat = True):
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
        telegram_token = os.environ['INPUT_TELEGRAM-TOKEN'],
        telegram_chat_id = os.environ['INPUT_TELEGRAM-CHAT-ID'],
        rocket_chat_url = os.environ['INPUT_ROCKET-CHAT-URL'],
        rocket_chat_token = os.environ['INPUT_ROCKET-CHAT-TOKEN'],
        rocket_chat_user_id = os.environ['INPUT_ROCKET-CHAT-USERID'],
        rocket_chat_channel = os.environ['INPUT_ROCKET-CHAT-TARGET-CHAT'],
        message_text = os.environ['INPUT_MESSAGE-TEXT'],
        enable_rocket_chat = os.environ['INPUT_ROCKET-CHAT'],
        enable_telegram = os.environ['INPUT_TELEGRAM'],
    )

def send_telegram_message(config: Config):
    print(config)
    assert config.enable_telegram == 'true' and config.telegram_token and config.telegram_chat_id and config.message_text
    url = f'https://api.telegram.org/bot{config.telegram_token}/sendMessage'
    data = {
        'chat_id': config.telegram_chat_id,
        'text': config.message_text,
        'parse_mode': 'HTML'
    }
    response = httpx.post(url, json=data)
    if response.status_code != 200:
        print(f'Error while posting message to Telegram \n{response.content}')
        print(response.text)
        sys.exit(1)

def send_rocket_chat_message(config: Config):
    assert config.enable_rocket_chat == 'true' and config.rocket_chat_url and config.rocket_chat_token and config.rocket_chat_user_id and config.rocket_chat_channel and config.message_text != None
    url = f'{config.rocket_chat_url}/api/v1/chat.postMessage'
    headers = {
        'X-Auth-Token': config.rocket_chat_token,
        'X-User-Id': config.rocket_chat_user_id,
        'Content-type': 'application/json'
    }
    data = {
        'channel': config.rocket_chat_channel,
        'text': config.message_text,
        'alias': 'Beep Boop',
        'avatar': 'https://img.freepik.com/premium-vector/cute-robot-waving-hand-cartoon-illustration_138676-2744.jpg?w=2000'
    }
    response = httpx.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f'Error while posting message to Rocket.Chat \n{response.content}')
        print(response.text)
        sys.exit(1)

def main():
    config = get_vars()
    if config.enable_telegram:
        send_telegram_message(config)
    if config.enable_rocket_chat:
        send_rocket_chat_message(config)

if __name__ == '__main__':
    main()
    print('Message sent successfully!')