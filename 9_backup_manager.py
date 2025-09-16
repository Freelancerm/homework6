import shutil
import os
import datetime


class BackupManager:
    """ Контекстний менеджер для створення резервних копій файлів. """

    def __init__(self, file_path):
        """
        Ініціалізує менеджер резервного копіювання.

        Args:
            file_path (str): Шлях до файлу, який потрібно обробити
        """
        self.file_path = file_path
        self.backup_path = None

    def __enter__(self):
        """ Створює резервну копію файлу """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Файл {self.file_path} не знайдено.")

        # Створюємо бекап файл у форматі: назва файлу.bak.дата
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.backup_path = f"{self.file_path}.bak.{timestamp}"

        shutil.copy2(self.file_path, self.backup_path)
        print(f"Створюємо резервну копію файлу: {self.backup_path}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Обробляє вихід із контексту, відновлює файл у разі помилки. """
        if exc_type is not None:
            # Виникла помилка, відновлюємо файл з резервної копії
            print(f"Виникла помилка: {exc_val}")
            if self.backup_path and os.path.exists(self.backup_path):
                shutil.move(self.backup_path, self.file_path)
                print("Файл відновлено з резервної копії.")
            else:
                print("Не вдалося відновити файл, резервна копія відсутня.")
            return False  # Поширюємо виняток
        else:
            print("Обробка файлу пройшла успішно.")
            if self.backup_path and os.path.exists(self.backup_path):
                os.remove(self.backup_path)
                print("Резервну копію видалено.")
        return True


# Приклад використання
if __name__ == "__main__":

    # Створення текстового файлу
    test_file = "test_file.txt"
    with open(test_file, 'w', encoding='utf-8') as file:
        file.write("Це оригінальний текст.")

    print("--- Сценарій 1: Успішна обробка ---")
    try:
        with BackupManager(test_file) as file:
            print(f"Обробляємо файл: {test_file}")
            with open(test_file, 'w', encoding='utf-8') as file_to_write:
                file_to_write.write("Це новий текст (в середині файлу) після успішної обробки")
    except Exception as ex:
        print(f"Сталася помилка: {ex}")

    print("\nПеревірка вмісту файлу після успішної обробки:")
    with open(test_file, 'r', encoding='utf-8') as file:
        print(file.read())

    print("\n--- Сценарій 2: Обробка з помилкою ---")
    try:
        with BackupManager(test_file) as file:
            print(f"Обробляємо файл: {test_file}")
            with open(test_file, 'w', encoding='utf-8') as file_to_write:
                file_to_write.write("Цей текст буде записано, але потім виникне помилка!")

    except ValueError as error:
        print(f"Виняток перехоплено в основній програмі: {error}")

    print("\nПеревірка вмісту файлу після помилки:")
    with open(test_file, 'r', encoding='utf-8') as file:
        print(file.read())
