# uvicorn app.main:app_v1 --reload
import os
import requests
from dotenv import load_dotenv
load_dotenv()
url = os.getenv('BASE_URL')

# Представление удаления вида транспорта
def delete_transport_view(transport_id):
    url_api = f'{url}/transports/delete/{transport_id}'

    # DELETE-запрос
    response = requests.delete(url_api)
    if response.status_code == 200:
        # Десериализация JSON-данных
        json_data = response.json()
        print(json_data)
    else:
        print(f'Ошибка запроса, статус: {response.status_code}')

delete_transport_view(5)