import threading, time, json
import vk_api, requests
import vk_communication, loader, school_website_parcer, logs
from vk_api.longpoll import VkLongPoll, VkEventType

main_token = "4ccef41dfe9ecc1cf815552f0e994b4652b1b7b84be3b1f88c3e308f05321dcad56af5157f51f6cebd6e0"

#main_token = "778892b40fb7f44a542d65a0ff71b5d8f3b948974829f349b252b8fe462a0e2c9a4204b94812a1b2b830a"

def send_all(token):
    while True:
        try:
            # Подключение к vk и паблику
            vk_session = vk_api.VkApi(token=token)
            vk = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            data = vk_session.method('messages.getLongPollServer',{'access_token': token})

            while True:
                current_date = ''
                lessons = {}
                try:
                    with open('data/lessons.json', 'r', encoding='UTF-8') as f:
                        lessons = json.load(f)
                except FileNotFoundError:
                    logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Lessons file not found error.')
                    continue

                current_date = lessons['date']
                
                with open('data/users.json', 'r', encoding='UTF-8') as f:
                    users = json.load(f)
                    for user in users:
                        if users[user]['up'] and users[user]['class'] != '-0-' and users[user]['date'] != current_date:
                            vk_communication.feedback(longpoll, vk, users[user]['id'], users[user]['class'])

                time.sleep(10)

        # Пересоеденение в случае ошибки
        except requests.exceptions.ConnectionError:
            logs.log('Recconect...')
        except:
            logs.log('Recconect...')
    

def logs_cleaner():
    while True:
        try:
            with open(logs.logs_file_name, 'w'):
                None
            with open(logs.errors_logs_file_name, 'w'):
                None
        except:
            None
        time.sleep(30*24*60)

if __name__ == '__main__':
    thread_vk = threading.Thread(target=vk_communication.vk_connection, args=[main_token])
    thread_vk_send_all = threading.Thread(target=send_all, args=[main_token])
    thread_load = threading.Thread(target=loader.loader, args=['data/lessons.json', 'data/temp.xls', 'https://s11028.edu35.ru/2013-06-12-15-17-31/raspisanie', ['.xls']])
    thread_cleaner = threading.Thread(target=logs_cleaner, args=[])
    
    thread_vk.start()
    thread_vk_send_all.start()
    thread_load.start()
    thread_cleaner.start()

    thread_vk.join()
    thread_vk_send_all.join()
    thread_load.join()
    thread_cleaner.join()
