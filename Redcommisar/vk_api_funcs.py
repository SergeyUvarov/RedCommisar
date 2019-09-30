import vk_api, json

import logs

""" create_begin_keyboard - создаёт клавиатуру смен с кнопкой быстрого набора """
def create_begin_keyboard(base_file, fast_button_text='-0-'):
    try:
        # Загрузка основы клавиатуры
        with open(base_file, 'r', encoding='UTF-8') as f:
            keyboard = json.load( f )
            
        # Вставка кнопок быстрого набора
        if not fast_button_text == '-0-':
            keyboard['buttons'][0].append({'action': { 'type': 'text', 'label': fast_button_text }, 'color': 'positive'})
            
        # Уборка лишних строк
        keyboard['buttons'] = [keyboard['buttons'] for keyboard['buttons'] in keyboard['buttons'] if keyboard['buttons']]
        return keyboard

    except json.decoder.JSONDecodeError:
        logs.error_log(create_begin_keyboard.__name__, [base_file, fast_button_text], 'Base JSON format decode error.')
    except FileNotFoundError:
        logs.error_log(create_begin_keyboard.__name__, [base_file, fast_button_text], 'File not found error.')
    except TypeError:
        logs.error_log(create_begin_keyboard.__name__, [base_file, fast_button_text], 'Input type error.')
    except:
        logs.error_log(create_begin_keyboard.__name__, [base_file, fast_button_text], 'Unknow error.')
    return False



""" create_froms_numbers_keyboard - создаёт клавиатуру из списка классов в смене """
def create_froms_numbers_keyboard(base_file, forms_list, time_part):
    try:
        # Загрузка основы клавиатуры
        with open(base_file, 'r', encoding='UTF-8') as f:
            keyboard = json.load( f )

        # Вставка кнопок по 4 в ряду 
        row, colm = 0, 0
        for forms_num in forms_list[time_part]:
            keyboard['buttons'][row].append({'action': { 'type': 'text', 'label': forms_num }, 'color': 'positive'})
            colm += 1
            if colm > 3:
                colm = 0
                row += 1
                
        # Уборка лишних строк
        keyboard['buttons'] = [keyboard['buttons'] for keyboard['buttons'] in keyboard['buttons'] if keyboard['buttons']]
        return keyboard

    except json.decoder.JSONDecodeError:
        logs.error_log(create_froms_numbers_keyboard.__name__, [base_file, forms_list, time_part], 'Base JSON format decode error.')
    except FileNotFoundError:
        logs.error_log(create_froms_numbers_keyboard.__name__, [base_file, forms_list, time_part], 'File not found error.')
    except TypeError:
        logs.error_log(create_froms_numbers_keyboard.__name__, [base_file, forms_list, time_part], 'Input type error.')
    except:
        logs.error_log(create_froms_numbers_keyboard.__name__, [base_file, forms_list, time_part], 'Unknow error.')
    return False
        


""" create_froms_alpha_keyboard - создаёт клавиатуру из списка паралелий в смене """
def create_froms_alpha_keyboard(base_file, forms_list, time_part, class_number):
    try:
        # Загрузка основы клавиатуры
        with open(base_file, 'r', encoding='UTF-8') as f:
            keyboard = json.load( f )

        # Вставка кнопок по 4 в ряду
        row, colm = 0, 0
        for forms_num in forms_list[time_part][class_number]:
            keyboard['buttons'][row].append({'action': { 'type': 'text', 'label': class_number + forms_num }, 'color': 'positive'})
            colm += 1
            if colm > 3:
                colm = 0
                row += 1
                
        # Уборка лишних строк
        keyboard['buttons'] = [keyboard['buttons'] for keyboard['buttons'] in keyboard['buttons'] if keyboard['buttons']]
        return keyboard

    except json.decoder.JSONDecodeError:
        logs.error_log(create_froms_alpha_keyboard.__name__, [base_file, forms_list, time_part, class_number], 'Base JSON format decode error.')
    except FileNotFoundError:
        logs.error_log(create_froms_alpha_keyboard.__name__, [base_file, forms_list, time_part, class_number], 'File not found error.')
    except TypeError:
        logs.error_log(create_froms_alpha_keyboard.__name__, [base_file, forms_list, time_part, class_number], 'Input type error.')
    except:
        logs.error_log(create_froms_alpha_keyboard.__name__, [base_file, forms_list, time_part, class_number], 'Unknow error.')
    return False
