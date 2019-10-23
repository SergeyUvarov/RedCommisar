from datetime import datetime
import json
import logs

month_base_name = "data/months.json"

""" get_month_id - переводит название месяца в его номер """
""" согласно базе months.json                            """
def get_month_id(month_name):
    try:
        month_name = month_name.lower()
        # Открытие базы
        with open(month_base_name, 'r', encoding="utf-8") as month_base_file:
            base = json.load(month_base_file)
            # Перебор всех месяцев
            for month_id in base:
                # Перебор всех вариантов записи одного месяца
                for text_variant in base[str(month_id)]:
                    # Совпадение
                    if text_variant.lower() == month_name:
                        return int(month_id)
        # Неизвестный вариант
        logs.error_log(get_month_id.__name__, [month_name], "Unknow month.")
        return False
    
    except AttributeError:
        logs.error_log(get_month_id.__name__, [month_name], "Uncorrect input data.")
    except json.decoder.JSONDecodeError:
        logs.error_log(get_month_id.__name__, [month_name], "Base decoding error.", [month_base_name])
    except FileNotFoundError:
        logs.error_log(get_month_id.__name__, [month_name], "Base does not exist.", [month_base_name])
    except TypeError:
        logs.error_log(get_month_id.__name__, [month_name], "Unccorect base data.", [month_base_name])
    except ValueError:
        logs.error_log(get_month_id.__name__, [month_name], "Unccorect base output.", [month_base_name])
    except:
        logs.error_log(get_month_id.__name__, [month_name], "Unknow error.")
    return False



""" get_date_id - возращает ID даты вида '1 сентября', """
""" где ID следующего деня больше предыдущего          """
def get_date_id(date_input):
    try:
        # Разбор даты на день и месяц
        date_parts = date_input.split()
        # Проверка на корректность месяца
        if(get_month_id(date_parts[1]) == False):
            logs.error_log(get_date_id.__name__, [date_input], "Month recognition error.")
            return False
        # Преобразование к числовым значениям
        day = int(date_parts[0])
        month = int( get_month_id(date_parts[1]) ) -1
        # Разбитие на ячейки по 31-ому дню
        date_id = day + month*31
        return date_id

    except ValueError:
        logs.error_log(get_date_id.__name__, [file_date], "Uncorrect input day format.")
    except:
        logs.error_log(get_date_id.__name__, [file_date], "Unknow error.")
    return False



""" get_now_date_id - возращает ID текущего дня """
def get_now_date_id():
    try:
        # Получение текущей даты в виде картежа
        current_date = datetime.today()
        format_date = current_date.timetuple()
        # Преобразование к числовым значениям
        day = format_date[2]
        month = format_date[1] -1
        # Разбитие на ячейки по 31-ому дню
        date_id = day + month*31
        return date_id
    
    except:
        logs.error_log(get_now_date_id.__name__, [current_date], "Unknow error.")
    return False
