import zipfile
import os


class ZipArchiveManager:
    """ Менеджер контексту для створення та управління ZIP-архівом. """

    def __init__(self, archive_name):
        self.archive_name = archive_name
        self.zip_file = None

    def __enter__(self):
        self.zip_file = zipfile.ZipFile(self.archive_name, 'w', zipfile.ZIP_DEFLATED)
        print(f"Створено новий архів: '{self.archive_name}'")
        return self

    def add_file(self, file_path, arcname=None):
        if self.zip_file:
            try:
                self.zip_file.write(file_path, arcname=arcname or os.path.basename(file_path))
                print(f"Додано файл: '{file_path}'")
            except FileNotFoundError:
                print(f"Помилка: Файл {file_path} не знайдено.")
        else:
            print("Помилка: Архів не відкритий. Використовуйте менеджер контексту.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.zip_file:
            self.zip_file.close()
            print(f"Архів '{self.archive_name}' успішно закритий.")
        return False


# Використання менеджеру контексту для створення архіву
archive_to_remove = "temp_archive.zip"

# Створення тестового файлу
with open("test_file.txt", 'w', encoding='utf-8') as file:
    file.write("Цей файл буде заархівовано")

try:
    with ZipArchiveManager(archive_to_remove) as zipper:
        zipper.add_file("test_file.txt")

    # Перевірка, чи існуж архів та його видалення
    if os.path.exists(archive_to_remove):
        os.remove(archive_to_remove)
        print(f"\nАрхів '{archive_to_remove}' успішно видалено.")
    else:
        print(f"\nАрхів '{archive_to_remove}' не знайдено.")

except Exception as ex:
    print(f"Виникла помилка:  {ex}")

finally:
    # Видалення текстового файлу
    if os.path.exists("test_file.txt"):
        os.remove("test_file.txt")
        print("Тестовий файл 'test_file.txt' видалено.")
