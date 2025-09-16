import os


def filter_lines(file_path, keyword):
    """
    Генератор, який читає великий текстовий файл рядок за рядком
    та повертає ті рядки, які мітять ключове слово 
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if keyword in line:
                    yield line
    except FileNotFoundError:
        print(f"Помилка: файл за шляхом '{file_path}' не знайдено.")
    except Exception as error:
        print(f"Виникла помилка при читанні файлу: {error}")


def process_and_clean_up(input_file, output_file, search_keyword):
    """
    Виконує фільтрацію файлу, виводить результат у консоль, зберігає його в новий
    файл, а потім видаляє всі створені файли після завершення роботи.
    """

    try:
        # Створюємо файл для демонстрації
        if not os.path.exists(input_file):
            print(f"Створення тестового файлу '{input_file}' ...'")
            with open(input_file, "w", encoding="utf-8") as file:
                file.write("INFO: Користувач 'admin' увійшов.\n")
                file.write("ERROR: не вдалося під'єднатись до бази даних.\n")
                file.write("INFO: Застосунок запущено успішно.\n")
                file.write("ERROR: Файл не знайдено.\n")
            print("Файл створено.")

        # Фільтруємо файл і виводимо результат
        print("\n--- Відфільтровані рядки ---")
        filtered_lines = list(filter_lines(input_file, search_keyword))
        for line in filtered_lines:
            # Виводимо рядок у консоль без зайвих пробілів
            print(line.strip())

        # Зберігаємо відфільтровані рядки у новий файл
        with open(output_file, "w", encoding="utf-8") as outuput_file:
            for line in filtered_lines:
                outuput_file.write(line)
        print(f"\nРезультат збережено у '{output_file}'")

    except Exception as error:
        print(f"Виникла помилка під час виконання: {error}")

    finally:
        # Видаляємо всі створені тимчасові файли
        print("\n--- Видалення тимчасових файлів ---")
        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"Файл '{output_file}' видалено.")
        else:
            print(f"Файл '{output_file}' не існує, видалення не потрібне.")


# Запуск програми:
input_file_path = "big_log.txt"
output_file_path = "filtered_log.txt"
searching_keyword = "ERROR"

process_and_clean_up(input_file_path, output_file_path, searching_keyword)
print("\nВидалення основного файлу з логами.")
if os.path.exists(input_file_path):
    os.remove(input_file_path)
    print(f"Файл '{input_file_path}' видалено.")
else:
    print(f"Файл '{input_file_path}' не існує, видалення не потрібне.")
