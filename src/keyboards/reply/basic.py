from src.keyboards.reply.default import DefaultConstructor


class BasicButtons(DefaultConstructor):
    @classmethod
    def menu(cls):
        schema = [2, 1]
        buttons = ["🔔 Уведомления", "⚙️ Настройки", "Кто сейчас свободен?"]
        return cls._create_kb(buttons, schema)
