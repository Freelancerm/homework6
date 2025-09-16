import os


def reverse_file_reader(filename):
    """
    Ітератор-генератор, який зчитує файл рядок за рядком у зворотному порядку
    """
    try:
        # Читаємо всі рядки у список
        with open(filename, 'r', encoding='utf-8') as fileline:
            lines = fileline.readlines()

        # Використовуємо reversed() для ітерації у зворотньому порядку
        # та yield для видачі рядків по одному
        for line in reversed(lines):
            yield line.strip()

    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
    except Exception as error:
        print(f"Сталася невідома помилка: {error}")


# Приклад використання
test_file_name = 'log.txt'
with open(test_file_name, 'w', encoding='utf-8') as file:
    file.write("Лог запис 1\n")
    file.write("Лог запис 2\n")
    file.write("Лог запис 3\n")
    file.write("Лог запис 4\n")
    file.write("Лог запис 5\n")

print(f"Зчитуання файлу {test_file_name} у зворотньому порядку:")
for log_entry in reverse_file_reader(test_file_name):
    print(log_entry)

# Видалення файлу після завершення програми
os.remove(test_file_name)
