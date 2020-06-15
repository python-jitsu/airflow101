import functools
from bot import Bot


class TelegramAlertHelper:
    def __init__(self, token, chat_id):
        self.bot = Bot(token)
        self.sendMessage = functools.partial(self.bot.sendMessage, chat_id=chat_id)

    def _get_task_context_str(self, context):
        return f'{context["task_instance_key_str"]}: {context["execution_date"]}'

    def on_success_callback(self, context):
        text = f'👍 Ура, мы смогли {self._get_task_context_str(context)}'
        self.sendMessage(text=text)

    def on_retry_callback(self, context):
        text = f'⭕️ Мы попробуем ещё раз {self._get_task_context_str(context)}'
        self.sendMessage(text=text)

    def on_failure_callback(self, context):
        text = f'️👎 Всё пропало {self._get_task_context_str(context)}'
        self.sendMessage(text=text)

    def on_sla_miss_callback(self, context):
        text = 'МЫ НЕ УСПЕЛИ НАТАША'
        self.sendMessage(text=text)