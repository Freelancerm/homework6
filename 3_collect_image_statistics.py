import csv
import io
import requests
import os
from PIL import Image


def image_metadata_generator(image_urls):
    """
    Генератор, який по черзі завантажує зображення за URL-адресою,
    витягує їх метадані та повертає у вигляді словника
    """
    for url in image_urls:
        try:
            print(f"Завантаження {url}")
            response = requests.get(url, timeout=10)
            # Перевірка на помилки HTTP
            response.raise_for_status()

            image_data = io.BytesIO(response.content)

            with Image.open(image_data) as image:
                metadata = {
                    'url': url,
                    'format': image.format,
                    'size_width': image.size[0],
                    'size_height': image.size[1],
                    'mode': image.mode
                }
                yield metadata
            print(f"Оброблено зображення: {url} ")
        except requests.exceptions.RequestException as error:
            print(f"Помилка завантаження '{url}': {error}")
        except Exception as error:
            print(f"Помилка при обробці зображення з '{url}': {error}")


def save_metadata_to_csv(metadata_generator, output_csv_file):
    """Зберігає метадані, отримані від генератора, у CSV файл"""
    all_metadata = []

    # Використовуємо список для тимчасового зберігання даних, щоб потім їх відобразити
    for metadata in metadata_generator:
        all_metadata.append(metadata)

    if not all_metadata:
        print("Генератор не містить даних для збереження.")
        return False

    try:
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = all_metadata[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_metadata)

        return True, all_metadata

    except IOError as error:
        print(f"Сталася помилка запису у файл {output_csv_file}: {error}")
        return False, None


def display_and_clean_up(output_csv_file, metadata_list):
    """ Відображає вміст файлу і потім видаляє його. """
    print("\n--- Вміст csv файлу ---")

    # Відображення заголовків
    if metadata_list:
        headers = metadata_list[0].keys()
        print(", ".join(headers))

        # Відображення даних
        for row in metadata_list:
            values = [str(v) for v in row.values()]
            print(", ".join(values))
    else:
        print("Файл порожній або не був створений.")

    print("-" * 50)
    # Видалення файлу
    if os.path.exists(output_csv_file):
        os.remove(output_csv_file)
        print(f"\n Файл '{output_csv_file} успішно видалено")
    else:
        print(f"Файл '{output_csv_file}' не знайдено для видалення.")


if __name__ == "__main__":
    image_links = [
        "https://images.nationalgeographic.org/image/upload/t_edhub_resource_key_image/v1638886301/EducationHub/photos/lightning-bolts.jpg",
        "https://resilience-blog.com/wp-content/uploads/2022/06/fig_management-1024x385.png",
        "https://assets.tommackie.com/wp-content/uploads/2021/05/25145056/180540-1-1-1536x1025.jpg",
        "https://assets.tommackie.com/wp-content/uploads/2021/05/25133421/180016-2.jpg"
    ]

    output_csv = 'online_image_stats.csv'

    # Створюємо генератор і передаємо його у функцію збереження
    metadata_gen = image_metadata_generator(image_links)
    result, meta_list = save_metadata_to_csv(metadata_gen, output_csv)

    # Якщо файл успішно створено, відображаємо його вміст та видаляємо.
    if result:
        display_and_clean_up(output_csv, meta_list)
    else:
        print("Обробку та відображення пропущено через помилку")
