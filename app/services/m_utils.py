
from app.config import settings


class ClassUtils:

    def __init__(self):
        self.MSGS1 = settings.MSGS1
        self.MSGS2 = settings.MSGS2


    async def add_dialog_stylist(self, content: str, role: str):
        message = {
            "role": role,
            "content": content
        }
        self.MSGS1.append(message)
        return self.MSGS1

    async def add_dialog_designer(self, content: str, role: str):
        message = {
            "role": role,
            "content": content
        }
        self.MSGS2.append(message)

    async def reset_dialog(self):
        self.MSGS1.clear()





UtilsClass = ClassUtils()


