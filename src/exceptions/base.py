class BaseAiogramTemplateError(Exception):
    """
    Base exception for all Aiogram bot template errors
    """


class DetailedAiogramTemplateError(BaseAiogramTemplateError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self}')"
