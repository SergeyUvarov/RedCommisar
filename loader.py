import requests, xlrd, json, time

import school_website_parcer, logs


""" to_json - конвертирует расписание в json файл """
def to_json(base, classes_lessons, date):
    try:
        # Открытие файла
        json_format = {}
        with open(base, 'r', encoding='UTF-8') as f:
            json_format = json.load(f)

        # Дозапись
        json_format['date'] = date # Дата расписания
        for form in classes_lessons:
            # Класс
            lessons = []
            form_class = form[0]
            form.remove(form_class)

            # Уроки
            for lesson in form:
                lessons.append(lesson)
            json_format[form_class] = lessons

        # Запись
        with open(base, 'w', encoding='UTF-8') as f:
            f.write( json.dumps(json_format, ensure_ascii=False, indent=4) )
            
    except:
        logs.error_log(to_json.__name__, [base, classes_lessons, date], 'Unknow error.')
    return False



""" excel_parcer - конвертирует таблицу с рассписанием в json """
def excel_parcer(output_file, temp, date):
    try:
        # Открытие загруженного расписания
        workbook = xlrd.open_workbook(temp)
        sheet = workbook.sheet_by_index(0)
        classes = []
        
        #Время уроков
        col = 2
        row = 2
        lessons = []
        if int(sheet.row_values(3)[1]) == 1:
            lessons.append('Время 1')
        else:
            lessons.append('Время 2')
            
	# Поиск времени уроков
        while row < sheet.nrows-1:
            row+=1
            if sheet.row_values(row)[col]:
                lessons.append(sheet.row_values(row)[col])
        classes.append(lessons)

        col = 3
        while col < sheet.ncols:
            row=2
            # Поиск классов
            if sheet.row_values(row)[col]:
                lessons = []
                lessons.append(sheet.row_values(row)[col].lower())
                row=1
                # Поиск уроков
                while row < sheet.nrows-2:
                    row+=2
                    lessons.append(sheet.row_values(row)[col].title())
                classes.append(lessons)
                
            col += 1
        # Сохранение расписание в json
        to_json(output_file, classes, date)

    except:
        logs.error_log(excel_parcer.__name__, [output_file, temp, date], 'Unknow error.')
    return False
    


""" loader - производит загрузку расписания в удобном формате """
def loader(output_file, temp_file, website_url, file_formats):
    while True:
        try:
            # Данные о расписании
            files = school_website_parcer.get_suitable_files_url(website_url, file_formats)
            time.sleep(5)
            # Загрузка
            for file in files:
                load = requests.get(file[0])
                with open(temp_file, 'wb') as f:
                    f.write(load.content)
                excel_parcer(output_file, temp_file, files[0][1])
                logs.log(file[0] + ' loaded')

        except:
            logs.error_log(loader.__name__, [output_file, temp_file, website_url, file_formats], 'Unknow error.')
        time.sleep(60)
