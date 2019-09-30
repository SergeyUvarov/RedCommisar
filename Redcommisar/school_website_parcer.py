from bs4 import BeautifulSoup, SoupStrainer
import requests
import time

import time_parcer
import logs


""" search_files_on_site - выдаёт кортеж URLs файлов с подходящими расширениеми """
def search_files_on_site(website_url, file_formats):
    try:
        if not file_formats:
            logs.error_log(search_files_on_site.__name__, [website_url, file_formats], "Empty file formats.")
            return False
        
        files_list = []
        # Подключение к сайту
        resources = requests.get(website_url, headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0' })
        soup = BeautifulSoup(resources.content, 'html.parser', parse_only=SoupStrainer('a'))
        # Получение всех ссылок на сайте
        links = [link['href'] for link in soup if link.has_attr('href')]
        # Поиск всех файлов с подходящими расширениеми
        for link in links:
            for file_format in file_formats:
                if file_format in link:
                    files_list.append(link)
                    
        if not files_list:
            logs.error_log(search_files_on_site.__name__, [website_url, file_formats], "No files found.", [links])
            return False
        print(files_list)
        return files_list

    except ConnectionError:
        logs.error_log(search_files_on_site.__name__, [website_url, file_formats], "Unable to connect to server.")
    #except:
        #logs.error_log(search_files_on_site.__name__, [website_url, file_formats], "Unknow error.")
    return False



""" get_file_name - выдаёт имя файла из его URL """
def get_file_name(file_url):
    try:
        # Полное имя Файла с форматом
        full_file_name = file_url.split('/')[-1]
        # Имя файла без его формата
        return full_file_name.split('.')[0]
    
    except:
        logs.error_log(get_file_name.__name__, [file_url], "Unknow error.")
    return False



""" correct_info_format - преобразует строку к единому формату """
def correct_info_format(file_name):
    try:
        format_str = ''
        last = file_name[0]
        begin = False
        # Избавление от лишних и недостающих пробелов
        file_name = file_name.replace(' ', '')
        for symb in file_name:
            # Начало с цифры
            if not begin and symb.isdigit():
                begin = True
            if begin:
                # Вставить пробел между числами и буквами
                if symb.isdigit() == last.isalpha() or last.isdigit() == symb.isalpha():
                    format_str += ' '
                # Избавление от не буквенно-численных символов
                if symb.isalnum():
                    format_str += symb
                last = symb
        return format_str.lower()
    
    except:
        logs.error_log(correct_info_format.__name__, [file_name], "Unknow error.")
    return False



""" get_date - выдаёт дату файла """
def get_date(file_name):
    try:
        # Разделение имени файла на части
        name_parts = file_name.split()
        if len(name_parts) < 2:
            logs.error_log(get_date.__name__, [file_name], "Uncorrect format.")
            return False
        # Соеденение дня и месяца в дату
        date = name_parts[0] + ' ' + name_parts[1]
        return date
    
    except:
        logs.error_log(get_date.__name__, [file_name], "Unknow error.")
    return False



""" get_suitable_files_url - выдаёт список URL файлов с актуальным расписанием """
def get_suitable_files_url(website_url, file_formats):
    #try:
        # База данных c расписанием в формате '[URL, дата, ID]'
        mini_base = []
        # Расписание на сегодня
        today = []
        # ID текущего дня
        current_date_id = time_parcer.get_now_date_id()
        # Все URL файлов с расписанием
        all_files_url = search_files_on_site(website_url, file_formats)
        time.sleep(5)
        if not all_files_url:
            logs.error_log(get_suitable_files_url.__name__, [website_url, file_formats], "Required files not found.")
            return False
        # Сортировка и обработка файлов расписания
        for file_url in all_files_url:
            cell = []
            # Получение даты расписания из его URL
            file_name = get_file_name(file_url)
            if not file_name:
                continue
            file_info = correct_info_format(file_name)
            if not file_info:
                continue
            date = get_date(file_info)
            if not date:
                continue
            # Получение его ID-даты
            date_id = time_parcer.get_date_id(date)
            if date_id:
                # Расписание на сегодня
                if date_id == current_date_id:
                    cell.append(file_url)
                    cell.append(date)
                    cell.append(date_id)
                    today.append(cell)
                # Расписание на следующие дни
                if date_id > current_date_id:
                    cell.append(file_url)
                    cell.append(date)
                    cell.append(date_id)
                    mini_base.append(cell)
            else:
                logs.error_log(get_suitable_files_url.__name__, [website_url, file_formats], "Uncorrect date format.", [file_url])
        
        # При отсутствии расписания на следующие дни, выдать расписание на сегодня
        if not mini_base:
            if today:
                return today
            else:
                return False
        # Поиск расписания на ближайший следующий день
        future_files = []
        lower = mini_base[0]
        for file in mini_base:
            if file[2] < lower[2]:
                lower = file
        for file in mini_base:
            if file[2] == lower[2]:
                future_files.append(file)
        return future_files
    
    #except:
        #logs.error_log(get_suitable_files_url.__name__, [website_url, file_formats], "Unknow error.")
    #return False
