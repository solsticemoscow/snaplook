import asyncio
import base64

import requests
from openai import OpenAI, AsyncOpenAI
from app.config import settings
from app.services.m_utils import UtilsClass


class ClassOAI:

    def __init__(self):
        self.llm = AsyncOpenAI(
            max_retries=3,
            timeout=15,
            base_url="https://api.proxyapi.ru/openai/v1",
            api_key=settings.OPENAI_API_PROXY
        )

        self.llm2 = AsyncOpenAI(
            max_retries=3,
            timeout=15,
            api_key=settings.OPENAI_API
        )

        self.vision = False

    async def get_text(self, MSGS: list):
        try:
            response = await self.llm.chat.completions.create(
                model=settings.MODEL_4O,
                messages=MSGS,
                max_tokens=700,
                temperature=0.7
            )
            ANSWER = response.choices[0].message.content
            return ANSWER
        except Exception as e:
            return e

    async def get_vision(
            self,
            image_path: str
    ):

        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY_SNAPLOOK}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": settings.PROMT2
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return e




    def get_text_4o(self, MSGS: list):
        try:

            response = self.llm.chat.completions.create(
                model="gpt-4o",
                messages=MSGS,
                max_tokens=700,
                temperature=0.7
            )

            ANSWER = response.choices[0].message

            return ANSWER


        except Exception as e:
            return e


ClassOpenAI = ClassOAI()


# async def f1():
#     return await UtilsClass.add_dialog_stylist(
#         content='https://i08.fotocdn.net/s214/893a2c375957cc87/public_pin_l/2881840177.jpg', role='user')
#
#
# res = asyncio.run(f1())
#
# async def f2():
#     return await ClassOpenAI.get_text(res)
#
#
# print(asyncio.run(f2()))

