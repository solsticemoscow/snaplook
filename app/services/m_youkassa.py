import json

from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from yookassa import Configuration, Refund, Settings
from app.config import settings

from yookassa import Payment

class ClassYouKassa:

    def __init__(self):
        Configuration.configure(settings.SHOP_ID, settings.YOUKASSA)


    def get_payment(self, payment_id: str):
        try:
            res = Payment.find_one(payment_id=payment_id)
            result = json.loads(res.json())
            return result['status']
        except Exception:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'Payment_id not found.',
            )

    def create_refund(self, sum: int, payment_id: str):
        try:
            res = Refund.create({
                "payment_id": payment_id,
                "description": "Не подошел размер",
                "amount": {
                    "value": str(sum),
                    "currency": "RUB"
                },
                "sources": [
                    {
                        "account_id": "456",
                        "amount": {
                            "value": str(sum),
                            "currency": "RUB"
                        }
                    }
                ]
            })
            result = json.loads(res.json())
            return result
        except Exception as e:
            return e


    def get_refund(self, refund_id: str):
        try:
            res = Refund.find_one(refund_id=refund_id)
            result = json.loads(res.json())
            return result
        except Exception:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f'Refund_id not found.',
            )



    def create_payment(self, sum: int = 10, description: str = 'test'):
        try:
            res = Payment.create(
                {
                    "amount": {
                        "value": sum,
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://merchant-site.ru/return_url"
                    },
                    "capture": True,
                    "description": description,
                    "metadata": {
                        'orderNumber': '72'
                    },
                    "receipt": {
                        "customer": {
                            "full_name": "Solstice",
                            "email": "solsticemoscow@ya.ru",
                            "phone": "79211234567",
                            "inn": "6321341814"
                        },
                        "items": [
                            {
                                "description": description,
                                "quantity": "1.00",
                                "amount": {
                                    "value": sum,
                                    "currency": "RUB"
                                },
                                "vat_code": "2",
                                "payment_mode": "full_payment",
                                "payment_subject": "commodity",
                                "country_of_origin_code": "RU",
                                "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                                "customs_declaration_number": "10714040/140917/0090376",
                                "excise": "20.00",
                                "supplier": {
                                    "name": "string",
                                    "phone": "string",
                                    "inn": "string"
                                }
                            },
                        ]
                    }
                }
            )

            result = json.loads(res.json())
            return result['id'], result["confirmation"]["confirmation_url"]
        except Exception as e:
            return e





ClassYK = ClassYouKassa()









