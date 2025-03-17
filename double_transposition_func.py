import random

def text_prep(text):
    """
    Подготавливает текст для шифрования:
    - Заменяет 'Ё' на 'Е'
    - Делает все буквы заглавными

    Args:
        text (str): Ключевое слово или фраза
    
    Returns:
        str: Форматированная строка
    """
    # Заменяем 'Ё' на 'Е' и делаем все буквы заглавными
    return text.upper().replace('Ё', 'Е')


def double_transposition_encrypt(plaintext, key1, key2):
    """
    Шифрует текст методом двойной перестановки.
    
    Args:
        plaintext (str): Текст для шифрования
        key1 (str): Первый ключ
        key2 (str): Второй ключ
    
    Returns:
        str: Зашифрованный текст
    """
    # Подготовка текста
    text = text_prep(plaintext)
    
    # Подготовка ключей
    key1 = text_prep(key1)
    key2 = text_prep(key2)
    
    # Определение размеров матрицы
    cols = len(key1)
    rows = len(key2)
    
    # Вычисляем общий размер матрицы
    matrix_size = cols * rows
    
    # Список специальных символов для заполнения
    special_chars = ['@', '#', '$', '%', '&', '*', '!', '?', '+', '=', '<', '>', '^', '~']
    
    # Дополняем текст, если его длина меньше размера матрицы
    if len(text) < matrix_size:
        padding_length = matrix_size - len(text)
        padding = ''.join(random.choice(special_chars) for _ in range(padding_length))
        text += padding
    
    # Создаем исходную матрицу, заполняя ее по строкам
    matrix = []
    for i in range(0, len(text), cols):
        row = text[i:i+cols]
        # Дополняем последнюю строку, если она неполная
        if len(row) < cols:
            padding_length = cols - len(row)
            padding = ''.join(random.choice(special_chars) for _ in range(padding_length))
            row += padding
        matrix.append(list(row))
    
    # Создаем перестановки для каждого ключа
    permutation1 = get_key_permutation(key1)
    permutation2 = get_key_permutation(key2)
    
    # Первая перестановка - перестановка столбцов
    # Для каждой строки матрицы меняем порядок символов согласно permutation1
    temp_matrix = []
    for row in matrix:
        # Создаем новую строку с переставленными элементами
        new_row = [''] * cols
        for i in range(cols):
            # permutation1[i] содержит индекс символа, который должен быть на i-ой позиции
            # Индексы в permutation начинаются с 1, поэтому вычитаем 1
            new_row[i] = row[permutation1[i] - 1]
        temp_matrix.append(new_row)
    
    # Вторая перестановка - перестановка строк
    # Создаем новую матрицу с переставленными строками согласно permutation2
    result_matrix = [[''] * cols for _ in range(rows)]
    for i in range(min(len(temp_matrix), rows)):
        # permutation2[i] содержит индекс строки, которая должна быть на i-ой позиции
        # Индексы в permutation начинаются с 1, поэтому вычитаем 1
        result_matrix[i] = temp_matrix[permutation2[i] - 1]
    
    # Преобразуем матрицу обратно в текст, считывая по строкам
    ciphertext = ''
    for row in result_matrix:
        ciphertext += ''.join(row)
    
    # return matrix, permutation1, permutation2
    return ciphertext

def get_key_permutation(key):
    """
    Возвращает список индексов перестановки для заданного ключа.
    
    Args:
        key (str): Ключ для перестановки
    
    Returns:
        list: Список с индексами исходных позиций в порядке сортировки
    """
    # Создаем список пар (символ, позиция)
    indexed_key = [(char, i) for i, char in enumerate(key, 1)]
    
    # Сортируем по символам
    sorted_indexed_key = sorted(indexed_key, key=lambda x: x[0])
    
    # Извлекаем исходные позиции в новом порядке
    permutation = [orig_pos for _, orig_pos in sorted_indexed_key]
    
    return permutation


# Тест шифрования
plaintext = 'ЕХАЛ ГРЕК ЧЕРЕ РЕКУ'
key1 = 'КЛЮЧ'
key2 = 'СТОЛ'
ciphertext = double_transposition_encrypt(plaintext, key1, key2)
print(ciphertext) 