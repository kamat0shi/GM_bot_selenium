from data import BOT_TOKEN,user1,user2
import requests
import time
from call import start, create_window_chat,url_Waaanther,url_pr1cechart,open_windows
TOKEN = BOT_TOKEN
API_URL = f'https://api.telegram.org/bot{TOKEN}'

def get_updates(offset=None):
    url = f'{API_URL}/getUpdates'
    params = {'offset': offset} if offset else {}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'result' in data:
            return data
        else:
            print(f"Unexpected response format: {data}")
            return {'result': []}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {'result': []}

def send_message(chat_id, text):
    url = f'{API_URL}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text, 'disable_notification': False}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Send message failed: {e}")

def get_user_id_by_username(username, chat_id):
    url = f'{API_URL}/getChatAdministrators'
    params = {'chat_id': chat_id}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'result' in data:
            admins = data['result']
            for admin in admins:
                if admin['user']['username'] == username:
                    return admin['user']['id']
        else:
            print(f"Unexpected response format: {data}")
    except requests.RequestException as e:
        print(f"Get chat administrators failed: {e}")
    return None

def main():
    # open_windows()
    offset = None
    while True:
        updates = get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                message_text = update.get('message', {}).get('text', '')
                chat_id = update.get('message', {}).get('chat', {}).get('id')
                if chat_id and '!gm' in message_text:
                    parts = message_text.split()
                    if len(parts) > 1:
                        user_mention = parts[1]
                        print(f'{user_mention=}')
                        if user_mention.startswith('@'):
                            user_mention = user_mention[1:]  
                        user_id = get_user_id_by_username(user_mention, chat_id)
                        if user_id:
                            try:
                                start(user_mention)
                                # Уведомление об успешной отправке в исходный чат
                                send_message(chat_id, f"Будим @{user_mention}!")
                            except Exception as e:
                                # Сообщение в исходный чат, если возникла ошибка
                                send_message(chat_id, f"Что-то пошло не так. Будите кэшаута или пробуйте еще раз. Ошибка: {e}")
                        else:
                            # Сообщение в исходный чат, если не удалось найти пользователя
                            send_message(chat_id, f"Не удалось найти пользователя с именем @{user_mention}.")
                offset = update['update_id'] + 1
        time.sleep(1)

if __name__ == '__main__':
    main()