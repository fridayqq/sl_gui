import streamlit as st
import requests
import datetime
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")

st.title("Заявка на создание/изменение инструкции")
st.markdown("Заполните данные ниже для создания заявки.")

# Поля ввода
task_type = st.selectbox(
    "Тип задачи",
    ["Создание новой инструкции", "Доработка существующей инструкции"]
)

zayavitel = st.text_area("Заявитель", "Введите свои ФИО / Уч. код")
subject = f"Подзадача на {task_type.lower()}"
description = st.text_area("Описание", "Введите описание задачи здесь (с указанием кода изделия / наименования инструкции / ccылки на инструкцию)")

full_description = f"Заявитель: {zayavitel}\n\n{description}"
# Get today's date
today = datetime.date.today()

# Update the date inputs
start_date = st.date_input("Дата начала", today)
due_date = st.date_input("Дата окончания", today + datetime.timedelta(days=45))

#type_href = st.text_input("Type Href", "/api/v3/types/13")
type_href = "/api/v3/types/13"
#status_href = st.text_input("Status Href", "/api/v3/statuses/1")
status_href = "/api/v3/statuses/1"
#parent_href = st.text_input("Parent Href", "/api/v3/work_packages/66")
parent_href = "/api/v3/work_packages/365"

# Add user dictionary
user_dict = {
    23: "Даниз Джафаров",
    18: "Андрей Шипилов",
    16: "Анжелика Турсунмуродова",
    10: "Александр Смолин",
    9: "Дмитрий Исаев",
    6: "Руслан Касимовский",
}

# Replace the assignee_href text input with this:
selected_user = st.selectbox(
    "Исполнитель",
    options=list(user_dict.values())
)

# Get the user ID for the selected name
user_id = [k for k, v in user_dict.items() if v == selected_user][0]
assignee_href = f"/api/v3/users/{user_id}"

if st.button("Создать подзадачу"):
    # Формирование данных запроса
    data = {
        "subject": subject,
        "description": {
            "format": "markdown",
            "raw": full_description
        },
        "type": {
            "href": type_href
        },
        "assignee": {
            "href": assignee_href
        },
        "startDate": start_date.strftime("%Y-%m-%d"),
        "dueDate": due_date.strftime("%Y-%m-%d"),
        "status": {
            "href": status_href
        },
        "parent": {
            "href": parent_href
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    # Отправка POST-запроса с базовой аутентификацией
    response = requests.post(api_url, headers=headers, json=data, auth=("apikey", api_key))
    
    if response.status_code == 201:
        response_data = response.json()
        # Извлекаем ID задачи из URL в ответе
        task_id = response_data.get('id') or response.headers.get('Location', '').split('/')[-1]
        st.success(f"Подзадача успешно создана! Номер задачи: {task_id}")
    else:
        st.error(f"Ошибка: {response.status_code} - {response.text}")
