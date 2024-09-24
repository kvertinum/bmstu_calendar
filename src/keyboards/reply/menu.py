from src.keyboards.reply.const import DefaultConstructor


class MenuButtons(DefaultConstructor):
    NOTIFICATIONS = "🔔 Уведомления"
    SETTINGS = "⚙️ Настройки"
    SCHEDULE = "🗓️ Расписание"
    FREE_STUDENTS = "Кто сейчас свободен?"

    SCHEDULE_TODAY = "🕓 Расписание на сегодня"
    SCHEDULE_WEEK = "🔄 Расписание не неделю"

    @classmethod
    def menu(cls):
        schema = [2, 1, 1]
        buttons = [
            cls.NOTIFICATIONS,
            cls.SETTINGS,
            cls.SCHEDULE,
            cls.FREE_STUDENTS
        ]
        return cls._create_kb(buttons, schema)
    
    @classmethod
    def schedule(cls):
        schema = [1, 1]
        buttons = [
            cls.SCHEDULE_TODAY,
            cls.SCHEDULE_WEEK
        ]
        return cls._create_kb(buttons, schema)
