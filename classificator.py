import pandas as pd
import os
from parser import parsing_data

# Структура директорий
dirs_2 = {
    'control': ['mk1', 'mk2a', 'mk2b', 'mk3'],
    'endo': ['mend1', 'mend2a', 'mend2b', 'mend3'],
    'exo': ['mexo1', 'mexo2a', 'mexo2b', 'mexo3']
}

# Создаем пустой список для хранения кусков данных (chunks)
all_dataframes = []

# Проходим по словарю: dir_1 - это ключ (control/endo/exo), sub_dirs - список папок
for dir_1, sub_dirs in dirs_2.items():
    for dir_2 in sub_dirs:
        print(f"Обрабатываю: {dir_1} / {dir_2}")
        
        # Вызываем ваш парсер для конкретной пары папок
        df_chunk = parsing_data(dir_1, dir_2)
        
        # Добавляем результат в список
        all_dataframes.append(df_chunk)

# Объединяем все куски в один большой DataFrame
# ignore_index=True нужен, чтобы пронумеровать строки заново (0, 1, 2...), а не дублировать индексы
df = pd.concat(all_dataframes, ignore_index=True)

# Проверяем результат
print("\nГотово! Первые 5 строк:")
print(df.head())

# (Опционально) Можно сохранить результат в csv, чтобы не парсить каждый раз заново
# df.to_csv('full_dataset.csv', index=False)