import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Налаштування Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_google_credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("your_google_sheet_name").sheet1

# Токен Telegram бота
TELEGRAM_TOKEN = 'your_telegram_bot_token'
TELEGRAM_API = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'

# Отримання оновлень від Telegram
def get_updates():
    url = f'{TELEGRAM_API}/getUpdates'
    response = requests.get(url)
    return json.loads(response.content)

# Відправка відповіді у Telegram
def send_message(chat_id, text):
    url = f'{TELEGRAM_API}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

# Головна функція
def main():
    updates = get_updates()
    
    for update in updates['result']:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            text = message['text']

            # Запис у Google Sheets
            sheet.append_row([text])

            # Відправка підтвердження назад у Telegram
            send_message(chat_id, 'Запис додано!')
        except Exception as e:
            print(f'Помилка: {e}')

if __name__ == '__main__':
    main()
