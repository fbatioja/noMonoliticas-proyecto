from .messages import Message

class IntegrationEvent(Message):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)