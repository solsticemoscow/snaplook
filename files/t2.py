import requests

# Make a GET request to the Wildeberries API
response = requests.get('https://api.wildeberries.ru/catalog/v1/categories')

# Check if the request was successful
if response.status_code == 200:

    print(response.text)

    data = response.json()

    # Access and print specific data from the response
    for category in data['categories']:
        print(category['name'])
else:
    print('Failed to retrieve data from the API')