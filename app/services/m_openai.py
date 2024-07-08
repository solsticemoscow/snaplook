
from openai import AsyncOpenAI
from app.config import settings



class ClassOAI:

    def __init__(self):
        self.llm = AsyncOpenAI(
            max_retries=3,
            timeout=15,
            api_key=settings.OPENAI_API_KEY_SNAPLOOK
        )


        self.vision = False

    async def get_text(self, MSGS: list):
        try:
            response = await self.llm.chat.completions.create(
                model="gpt-4o",
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

        response = await self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_path,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content





ClassOpenAI = ClassOAI()






