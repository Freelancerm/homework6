import contextlib
import os


def even_numbers_generator():
    """ Генерує нескінченну кількість парних чисел """
    num = 0
    while True:
        yield num
        num += 2


@contextlib.contextmanager
def even_numbers_file_writer(filename, limit):
    """
    Контекстний менеджер який записує парні числа у файл,
    приймає та лімітує кількість чисел
    """
    file = None
    try:
        file = open(filename, "w", encoding="utf-8")
        even_gen = even_numbers_generator()
        for _ in range(limit):
            file.write(str(next(even_gen)) + '\n')
        yield file
    finally:
        if file:
            file.close()


# Приклад використання
if __name__ == "__main__":
    file_name = 'even_numbers.txt'
    # Використовуємо context manager для генерації та запису чисел до файлу
    with even_numbers_file_writer(file_name, 100) as data:
        print(f"Файл '{file_name}' створено зі 100 першими парними числами")

    # Зчитуємо файл та виводимо його зміст у консоль:
    try:
        print("\n--- Вміст файлу: ---")
        with open(file_name, "r", encoding="utf-8") as input_file:
            for line in input_file:
                print(line.strip())
    except FileNotFoundError:
        print(f"Файл '{file_name}' не знайдено.")

    # Видаляємо файл
    try:
        os.remove(file_name)
        print(f"Файл '{file_name}' успішно видалено.")
    except OSError as error:
        print(f"Помилка: {error.strerror}. Помилка при спробі видалити файл: {file_name}.")
