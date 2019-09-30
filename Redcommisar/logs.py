from datetime import datetime

print_mode = True

logs_file_name = 'logs/logs.txt'
errors_log_file_name = 'logs/errors.txt'

""" log - записывает сообщение """
def log(message):
    with open(logs_file_name, 'a') as logs_file:
        text = '[' + str(datetime.today()) + '] ' + str(message)
        logs_file.write(text + '\n')
        if print_mode:
            print(text)

""" error_log - записывает сообщение об ошибке """
def error_log(func_name, input_data, error_type, clarification=[]):
    with open(errors_log_file_name, 'a') as elogs_file:
        text = '[' + str(datetime.today()) + ']\t\tFunc:' + str(func_name) + '\t\tInput:' + str(input_data) + '\t\tError:' + str(error_type) + '\t\tClarifications:' + str(clarification)
        elogs_file.write(text + '\n')
        if print_mode:
            print(text)
