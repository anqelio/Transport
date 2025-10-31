# uvicorn app.main:app_v1 --reload
import os
import requests
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('BASE_URL')

# Представление вывода вида транспорта по ID
def get_transport_view(transport_id):
    url_api = f'{url}/transport/get/{transport_id}'

    # GET-запрос
    response = requests.get(url_api)
    if response.status_code == 200:
        # Десериализация JSON-данных
        json_data = response.json()
        print(json_data)
    else:
        print(f'Ошибка запроса, статус: {response.status_code}')

get_transport_view(2)