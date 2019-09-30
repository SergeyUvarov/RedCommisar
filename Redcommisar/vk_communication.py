from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api, requests, json, random

import logs, vk_api_funcs, school_website_parcer

forms_file = 'data/forms.json'
user_base_file = 'data/users.json'
keyboard_base_file = 'data/keyboard_base.json'
keyboard_main_file = 'data/keyboard_0.json'
lessons_file = 'data/lessons.json'

""" found_class - возращает класс если он есть в строке """
def found_class(forms_file, text):
    for time_part in forms_file:
        for num in forms_file[time_part]:
            for lit in forms_file[time_part][num]:
                if num+lit in text:
                    return num+lit
    return False


""" feedback - ответ на сообщения """
def feedback(longpoll, vk, user_id, text):
    #try:
        # Список классов
        try:
            with open(forms_file, 'r', encoding='UTF-8') as f:
                forms = json.load(f)
        except FileNotFoundError:
            logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Forms list file not found error.')
            return False

        # Кнопка быстрого набора
        fast_key = '-0-'
        try:
            with open(user_base_file, 'r', encoding='UTF-8') as f:
                users = json.load(f)
                fast_key = users[str(user_id)]
        except: None

        
        if text in forms['1']:
            keyboard_classes = vk_api_funcs.create_froms_alpha_keyboard(keyboard_base_file, forms, '1', text)
            if not keyboard_classes:
                logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Classes 1 keyboard create error.')
                return False
            
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message='Классы:',
                keyboard=json.dumps(keyboard_classes)
            )

        elif text in forms['2']:
            keyboard_classes = vk_api_funcs.create_froms_alpha_keyboard(keyboard_base_file, forms, '2', text)
            if not keyboard_classes:
                logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Classes 2 keyboard create error.')
                return False
            
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message='Классы:',
                keyboard=json.dumps(keyboard_classes)
            )
                    
        elif text == '1 смена':
            keyboard_1 = vk_api_funcs.create_froms_numbers_keyboard(keyboard_base_file, forms, '1')
            if not keyboard_1:
                logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Forms 1 keyboard create error.')
                return False
            
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message='Паралели:',
                keyboard=json.dumps(keyboard_1)
            )

        elif text == '2 смена':
            keyboard_2 = vk_api_funcs.create_froms_numbers_keyboard(keyboard_base_file, forms, '2')
            if not keyboard_2:
                logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Forms 2 keyboard create error.')
                return False
            
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message='Паралели:',
                keyboard=json.dumps(keyboard_2)
            )

        elif text == 'Информация':
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message='Red_C0mmisar v3.1\nПо предложениям и техническим вопросам обращайтесь:\nhttps://vk.com/id171948783',
            )

        elif text == 'Помощь':
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message='/setfast {ваш класс} - добавить кнопку быстрого набора\n'
                        '/setfast # - убрать кнопку быстрого набора',
            )

        elif '/setfast #' in text.lower():
            # Удаление кнопки быстрого набора
            try:
                with open(user_base_file, 'r', encoding='UTF-8') as f:
                    users = json.load(f)
                    users[str(user_id)] = '-0-'
                with open(user_base_file, 'w', encoding='UTF-8') as f:
                    json.dump(users, f, ensure_ascii=False)
                vk.messages.send(
                    user_id=user_id,
                    random_id=random.getrandbits(64),
                    message = 'Конфигурация сохранена'
                )
            except:
                vk.messages.send(
                    user_id=user_id,
                    random_id=random.getrandbits(64),
                    message = 'Не удалось сохранить конфигурацию'
                )

        elif '/setfast ' in text: 
            # Поиск класса в команде
            try:
                form = found_class(forms, text.lower())
                if form:
                    with open(user_base_file, 'r', encoding='UTF-8') as f:
                        users = json.load(f)
                        users[str(user_id)] = form
                    with open(user_base_file, 'w', encoding='UTF-8') as f:
                        json.dump(users, f, ensure_ascii=False)
                    vk.messages.send(
                            user_id=user_id,
                            random_id=random.getrandbits(64),
                            message = 'Конфигурация сохранена'
                        )
                else:
                    vk.messages.send(
                        user_id=user_id,
                        random_id=random.getrandbits(64),
                        message = 'Не удалось сохранить конфигурацию'
                    )   
            except:
                vk.messages.send(
                    user_id=user_id,
                    random_id=random.getrandbits(64),
                    message = 'Не удалось сохранить конфигурацию'
                )

        elif found_class(forms, text.lower()):
            keyboard_main = vk_api_funcs.create_begin_keyboard(keyboard_main_file, fast_key)
            if not keyboard_main:
                logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Main keyboard create error.')
                return False
            
            # Загрузка расписания
            lessons = {}
            try:
                with open(lessons_file, 'r', encoding='UTF-8') as f:
                    lessons = json.load(f)
            except FileNotFoundError:
                logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Lessons file not found error.')
                return False

            # Формирование текста из расписания
            lessons_list = ''
            form = found_class(forms, text.lower())
            if not lessons[form]:
                vk.messages.send(
                    user_id=user_id,
                    random_id=random.getrandbits(64),
                    message = 'Нет расписания',
                    keyboard = json.dumps(keyboard_main)
                )
                return

            les_time = 1
            for lesson in lessons[form]:
                if lesson:
                    lessons_list += str(les_time) + '. ' + lesson.upper() + '\n'
                else:
                    lessons_list += str(les_time) + '. *****\n'
                les_time += 1
                    
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message = form + ' - ' + lessons['date'] + '\n===============\n' + lessons_list,
                keyboard = json.dumps(keyboard_main)
            ) 

                    
        else:
            keyboard_main = vk_api_funcs.create_begin_keyboard(keyboard_main_file, fast_key)
            if not keyboard_main:
                logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Main keyboard create error.')
                return False
            
            vk.messages.send(
                user_id=user_id,
                random_id=random.getrandbits(64),
                message='Меню выбора',
                keyboard=json.dumps(keyboard_main)
            ) 
            
    #except:
        #logs.error_log(feedback.__name__, [longpoll, vk, user_id, text], 'Unknow error.')
    #return False 



""" is_ingoing - является ли сообщение входящим """
def is_ingoing(element):
    flag = element[2]
    return not flag & 2



""" vk_connection - обрабатывает личные сообщения в VK """
def vk_connection(token):
    save_message = []
    
    # Бесконечная прослушка
    while True:
        try:
            # Подключение к vk и паблику
            vk_session = vk_api.VkApi(token=token)
            vk = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            data = vk_session.method('messages.getLongPollServer',{'access_token': token})

            # Если после пересоеденения остались сообщения, обработать их
            if len(save_message):
                feedback(longpoll, vk, save_message[0], save_message[1])

            # Прослушка
            while True:
                # Получение событий
                response = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(server=data['server'], key=data['key'], ts=data['ts'])).json()
                try:
                    updates = response['updates']
                except KeyError:
                    data = vk_session.method('messages.getLongPollServer',{'access_token': token})

                # Просмотр всех полученых событий
                for element in updates:
                    action_code = element[0]
                    # Если это входящее сообщение
                    if action_code == 4 and is_ingoing(element):
                        user_id = element[3]
                        text = element[5]
                        logs.log('New message from ' + str(user_id))
                        if text:
                            # Сохранение сообщения на всякий случай
                            save_message = [user_id, text]
                            # Реакция на сообщение
                            feedback(longpoll, vk, user_id, text)
                            # Всё хорошо, резервное сообщение больше не нужно
                            save_message = []

                # Все события обработанны, идём дальше  
                data['ts'] = response['ts']

            # Пересоеденение в случае ошибки

        except requests.exceptions.ConnectionError:
            logs.log('Recconect...')
        except:
            logs.log('Recconect...')
