
ID = 174824317
_short_id = ID // 100000

if 0 <= _short_id <= 143:
    basket = '01'
elif 144 <= _short_id <= 287:
    basket = '02'
elif 288 <= _short_id <= 431:
    basket = '03'
elif 432 <= _short_id <= 719:
    basket = '04'
elif 720 <= _short_id <= 1007:
    basket = '05'
elif 1008 <= _short_id <= 1061:
    basket = '06'
elif 1062 <= _short_id <= 1115:
    basket = '07'
elif 1116 <= _short_id <= 1169:
    basket = '08'
elif 1170 <= _short_id <= 1313:
    basket = '09'
elif 1314 <= _short_id <= 1601:
    basket = '10'
elif 1602 <= _short_id <= 1655:
    basket = '11'
elif 1656 <= _short_id <= 1919:
    basket = '12'
elif 1920 <= _short_id <= 2045:
    basket = '13'
elif 2046 <= _short_id <= 2189:
    basket = '14'
elif 2190 <= _short_id <= 2405:
    basket = '15'
else:
    basket = '16'

"""Делаем список всех ссылок на изображения и переводим в строку"""
link_str = f"https://basket-{basket}.wb.ru/vol{_short_id}/part{ID // 1000}/{ID}/images/big/1.jpg"
print(link_str)