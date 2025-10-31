# uvicorn app.main:app_v1 --reload
import os
import requests
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('BASE_URL')

# Представление добавления вида транспорта
def show_transport_view():
    url_api = f'{url}/transports/show'

    # GET-запрос
    response = requests.get(url_api)
    if response.status_code == 200 or response.status_code == 201:
        # Десериализация JSON-данных
        json_data = response.json()
        for i in json_data:
            print(i)
    else:
        print(f'Ошибка запроса, статус: {response.status_code}')

show_transport_view()