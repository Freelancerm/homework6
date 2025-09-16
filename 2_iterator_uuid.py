import uuid


def unique_id_generator():
    """
    Ітератор-генератор, який створює унікальні UUID/
    Кожен виклик генерує новий, унікальний ідентифікатор.
    """
    while True:
        yield uuid.uuid4()


# Приклад використання:
id_gen = unique_id_generator()

print("\nГенеруємо 5 унікальних івентифікаторів:")
for _ in range(5):
    print(next(id_gen))

print("\nГенеруємо ще 3 ідентифікатори:")
print(next(id_gen))
print(next(id_gen))
print(next(id_gen))
