import threading, time

import vk_communication, loader

main_token = "4ccef41dfe9ecc1cf815552f0e994b4652b1b7b84be3b1f88c3e308f05321dcad56af5157f51f6cebd6e0"

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
    thread_load = threading.Thread(target=loader.loader, args=['data/lessons.json', 'data/temp.xls', 'https://s11028.edu35.ru/2013-06-12-15-17-31/raspisanie', ['.xls']])
    thread_cleaner = threading.Thread(target=logs_cleaner, args=[])
    
    thread_vk.start()
    thread_load.start()
    thread_cleaner.start()

    thread_vk.join()
    thread_load.join()
    thread_cleaner.join()
