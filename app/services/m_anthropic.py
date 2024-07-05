import base64
import numpy as np

import anthropic
import httpx

from BOT.config import OPENAI_API_PROXY


class Anthropic:

    def __init__(self):
        self.anthropic_api = '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'

        self.proxy = OPENAI_API_PROXY

        self.client = anthropic.Anthropic(
            api_key=self.proxy,
        )

    def get_api(self):
        self.message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=700,
            temperature=0.7,
            system="Your task is to analyze the provided Python code snippet, identify any bugs or errors present, and provide a corrected version of the code that resolves these issues. Explain the problems you found in the original code and how your fixes address them. The corrected code should be functional, efficient, and adhere to best practices in Python programming.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "ты понимаешь русский?"
                        }
                    ]
                }
            ]
        )
        return self.message.content[0].text

    def get_vision(self):
        image2_url = "https://storage.yandexcloud.net/sol/FILES/IMAGES/chrome_5Q1cjq5tDl.jpg"
        image2_data = base64.b64encode(httpx.get(image2_url).content).decode("utf-8")

        self.message = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image2_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "найди и пришли весь текст."
                        }
                    ],
                }
            ],
        )

        return self.message.content[0].text

    def get_embendings(self):

        documents = [
            "В маркетплейсе Мегамаркет вы можете купить mortal Kombat 11 (XI) Ultimate (PS4) по выгодной цене."
        ]

        vo = voyageai.Client(api_key='pa-nQfG8x7L3S0PGNeX7Mgc500FyAd-zAwSa3S92-CRZ7I')
        # This will automatically use the environment variable VOYAGE_API_KEY.
        # Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

        doc_embds = vo.embed(
            texts=documents, model="voyage-2", input_type="document"
        ).embeddings


        query = "Какой маркетплейс?"


        # Embed the query
        query_embd = vo.embed(
            [query], model="voyage-2", input_type="query"
        ).embeddings[0]

        print(query_embd)

        # Compute the similarity
        # Voyage embeddings are normalized to length 1, therefore dot-product
        # and cosine similarity are the same.
        similarities = np.dot(doc_embds, query_embd)
        print(similarities)

        retrieved_id = np.argmax(similarities)
        print(documents[retrieved_id])


ClassAnthropic = Anthropic()

print(ClassAnthropic.get_embendings())





# import subprocess
# import requests
#
# json_data = {
#     'name': 'Hello World',
# }
#
# response = requests.post(
#     'https://europe-central2-search-423402.cloudfunctions.net/function-ai',
#     json=json_data,
#     timeout=70,
# )
#
# print(response.text)
