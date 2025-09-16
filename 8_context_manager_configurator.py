import json
import configparser
import os
from typing import Dict, Any


class UniversalConfigManager:
    """
    Універсальний конекстний менеджер для файлів конфігурацій (.json або .ini).
    Автоматично завантажує дані при вході та зберігає при виході.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.config_data = None
        self.file_type = file_path.split('.')[-1].lower()

    def __enter__(self):
        """ Завантажує дані з файлу в залежності від його розширення. """
        if self.file_type == 'json':
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w', encoding='utf-8') as config_file:
                    json.dump({}, config_file)
            with open(self.file_path, 'r', encoding='utf-8') as json_f:
                self.config_data = json.load(json_f)
        elif self.file_type == 'ini':
            self.config_data = configparser.ConfigParser()
            self.config_data.read(self.file_path)
        else:
            raise ValueError(f"Непідтримуваний тип файлу: {self.file_type}")

        return self.config_data

    def __exit__(self, ex_type, exc_val, exc_tb):
        """ Записує оновлені дані назад у файл """
        if self.file_type == 'json':
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.config_data, file, indent=4)
        elif self.file_type == 'ini':
            with open(self.file_path, 'w') as file:
                self.config_data.write(file)

        print(f"\nЗміни збережено у файлі: {self.file_path}")


# Приклад використання
if __name__ == "__main__":
    json_file = 'demo_config.json'
    ini_file = 'demo_settings.ini'

    # Створюємо та працюємо з JSON файлом
    print("--- Робота з JSON файлом ---")
    with UniversalConfigManager(json_file) as config:
        # Явно вказуємо що config є словником
        config: Dict[str, Any] = config

        config['database'] = {
            'host': 'localhost',
            'port': 5432
        }
        config['api_key'] = 'your_secret_key'
        print("Внесені зміни в JSON-об'єкт:", config)

    # Перевіряємо вміст файлу після завершення
    with open(json_file, 'r', encoding='utf-8') as file_json:
        print("Остаточний вміст файлу", json_file)
        print(file_json.read())

    print("-" * 30)

    # Створюємо та працюємо з INI файлом
    print("--- Робота з INI файлом ---")
    with UniversalConfigManager(ini_file) as settings:
        settings['SERVER'] = {
            'host': '127.0.0.1',
            'port': '8080'
        }
        settings['LOGGING'] = {
            'level': 'INFO',
            'file': 'app.log'
        }
        print("Внесені зміни в INI-об'єкт:", settings.sections())

    # Перевіряємо вміст файлу після завершення
    with open(ini_file, 'r', encoding='utf-8') as file_ini:
        print("Остаточний вміст файлу", ini_file)
        print(file_ini.read())

    print("-" * 30)

    # Видаляємо створені файли
    print("--- Видалення файлів ---")
    if os.path.exists(json_file):
        os.remove(json_file)
        print(f"Файл {json_file} видалено.")

    if os.path.exists(ini_file):
        os.remove(ini_file)
        print(f"Файл {ini_file} видалено.")
