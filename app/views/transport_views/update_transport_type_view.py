# uvicorn app.main:app_v1 --reload
import os
import requests
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('BASE_URL')

# Представление добавления вида транспорта
def update_transport_view(transport_id, name):
    url_api = f'{url}/transports/update/{transport_id}'
    transport = {
        'name_transport': name
        }
    # PUT-запрос
    response = requests.put(url_api, json=transport)
    if response.status_code == 200 or response.status_code == 201:
        # Десериализация JSON-данных
        json_data = response.json()
        print(json_data)
    else:
        print(f'Ошибка запроса, статус: {response.status_code}')

update_transport_view(1, 'Электропоезд')