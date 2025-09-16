import re
import os


def parse_log(log_file_path):
    """" Генератор, що зчитує лог-файл і повертає рядки з помилками (4хх або 5хх) """
    # Патерн для пошуку HTTP статусу 4xx або 5хх
    error_pattern = re.compile(r'HTTP/1.1"\s[45]\d{2}')

    with open(log_file_path, 'r') as file:
        for line in file:
            if error_pattern.search(line):
                yield line.strip()


# Шляхи до файлів
input_log_file = 'access.log'
output_errors_file = 'errors.log'

try:
    # Створення лог-файлу для прикладу
    with open(input_log_file, 'w', encoding='utf-8') as log:
        log.write('127.0.0.1 - - [10/Nov/2023:14:00:00 +0200] "GET /home HTTP/1.1" 200 1234 "-" "Mozilla/5.0"\n')
        log.write('192.168.1.1 - - [10/Nov/2023:14:00:01 +0200] "GET /images/logo.png HTTP/1.1" 200 5678 "-" "Mozilla/5.0"\n')
        log.write('127.0.0.1 - - [10/Nov/2023:14:00:02 +0200] "GET /nonexistent-page HTTP/1.1" 404 987 "-" "Mozilla/5.0"\n')
        log.write('10.0.0.5 - - [10/Nov/2023:14:00:03 +0200] "POST /api/data HTTP/1.1" 500 123 "-" "Mozilla/5.0"\n')
        log.write('8.8.8.8 - - [10/Nov/2023:14:00:04 +0200] "GET /about HTTP/1.1" 200 4321 "-" "Mozilla/5.0"\n')

    # Запис помилок в окремий файл
    with open(output_errors_file, 'w', encoding='utf-8') as error_file:
        for error_line in parse_log(input_log_file):
            error_file.write(error_line + '\n')
    print(f"Парсинг завершено. Знайдені помилки записані у файл '{output_errors_file}'.")

    # Виведення вмісту errors.log:
    print(f"\nВміст файлу '{output_errors_file}':")
    with open(output_errors_file, 'r', encoding='utf-8') as error_file:
        print(error_file.read())

finally:
    # Видалення файлів у блоці 'finally'
    try:
        if os.path.exists(input_log_file):
            os.remove(input_log_file)
            print(f"Файл '{input_log_file}' успішно видалено.")

        if os.path.exists(output_errors_file):
            os.remove(output_errors_file)
            print(f"Файл '{output_errors_file}' успішно видалено.")
    except OSError as error:
        print(f"Помилка видалення файлів: {error}")
