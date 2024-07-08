import base64

import azure.functions as func


import requests
from openai import OpenAI

app = func.FunctionApp()

class ClassOAI:

    def __init__(self):
        self.llm = OpenAI(
            max_retries=3,
            timeout=15,
            api_key='sk-proj-jRKGH5SgNyMvuKPkRz3MT3BlbkFJ9n1UknvcU80zePpEOhgN'
        )


        self.vision = False

    def get_text(self, MSGS: list):
        try:
            response = self.llm.chat.completions.create(
                model="gpt-4o",
                messages=MSGS,
                max_tokens=700,
                temperature=0.7
            )
            ANSWER = response.choices[0].message.content
            return ANSWER
        except Exception as e:
            return e

    def get_vision(
            self,
            image_path: str
    ):

        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

        base64_image = encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer sk-proj-jRKGH5SgNyMvuKPkRz3MT3BlbkFJ9n1UknvcU80zePpEOhgN"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": 'Опиши подробно, что ты вдишь на фото.'
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





ClassOpenAI = ClassOAI()


@app.function_name(name="HttpTrigger1")
@app.route(route="/", auth_level=func.AuthLevel.ANONYMOUS)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    print(ClassOpenAI.get_vision(image_path='https://mur-mur.top/uploads/posts/2023-03/1680268722_mur-mur-top-p-strogii-obraz-krasivo-70.jpg'))

    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
        )