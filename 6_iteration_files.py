import os
import tempfile
import shutil


class DirectoryFileIterator:
    """ Ітератор, який повертає назву та розмір кожного файлу в заданому каталозі. """

    def __init__(self, directory_path):
        """ Ініціалізує ітератор зі списком файлів у каталозі. """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Шлях не є каталогом: {directory_path}")

        self._directory = directory_path
        self._files = [
            os.path.join(directory_path, filename)
            for filename in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, filename))
        ]
        self._index = 0

    def __iter__(self):
        """ Повертає сам об'єкт ітератора """
        return self

    def __next__(self):
        """
        Повертає наступний елемент ітерації.
        Видає StopIteration, коли файли закінчуються.
        """
        if self._index >= len(self._files):
            raise StopIteration

        file_path = self._files[self._index]
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        self._index += 1

        return file_name, file_size


# Приклад використання
def main():
    """ Функція для демонстрації ітератора """
    temp_dir = tempfile.mkdtemp()
    print(f"Тимчасовий каталог: {temp_dir}\n")

    # Створюємо кілька тестових файлів
    try:
        with open(os.path.join(temp_dir, "file1.txt"), "w") as file:
            file.write("Це перший файл.")

        with open(os.path.join(temp_dir, "file2.dat"), "wb") as file:
            file.write(b"\x00" * 1024)  # Файл розміром 1 КБ

        with open(os.path.join(temp_dir, "file3.empty"), "w"):
            pass  # Порожній файл

        # Використовуємо наш ітератор для перебору каталогу
        file_iterator = DirectoryFileIterator(temp_dir)

        print("Файли в каталозі:")
        print("-" * 20)
        for file_name, file_size in file_iterator:
            print(f"Назва: {file_name}, Розмір: {file_size} байт")

    finally:
        # Видаляємо тимчасовий каталог та всі його файли
        shutil.rmtree(temp_dir)
        print(f"\nТимчасовий каталог '{temp_dir}' видалено.")


if __name__ == "__main__":
    main()
