from typing import Union

import requests


class Bot:
    BASE_URL = 'https://api.telegram.org'

    def __init__(self, token: str) -> None:
        self.token = token
        self.base_url = f'{self.BASE_URL}/bot{token}'

    def sendMessage(
        self,
        chat_id: Union[str, int],
        text: str,
        parse_mode: str = 'Markdown',
        disable_notification: bool = True,
    ) -> None:
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification,
        }
        response = requests.post(
            f'{self.base_url}/sendMessage', json=payload, timeout=3
        )
        return response.json()
