import pandas as pd
import os
import matplotlib.pyplot as plt
from parser import parsing_data

dirs_2 = {
    'control': ['mk1', 'mk2a', 'mk2b', 'mk3'],
    'endo': ['mend1', 'mend2a', 'mend2b', 'mend3'],
    'exo': ['mexo1', 'mexo2a', 'mexo2b', 'mexo3']
}

def visualize_file(filename):
    """
    Визуализирует данные из CSV или TXT файла.
    
    Параметры:
    filename: путь к файлу
    """
    # Проверка существования файла:
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return
    
    # Загрузка данных и создание фигуры с графиком
    # Определяем тип файла и читаем соответствующим образом
    if filename.endswith('.txt'):
        # Для txt: разделитель - пробелы, пропускаем первую строку (заголовок), задаем имена колонок
        names_columns = ['X', 'Y', 'Wave', 'Intensity', 'cat', 'feature_1', 'feature_2', 'feature_3', 'side']
        df = pd.read_csv(filename, delim_whitespace=True, skiprows=1, names=names_columns)
    else:
        # Для csv: стандартное чтение
        df = pd.read_csv(filename)
        
    print(f"\nЗагружен файл: {filename}")
    print(f"Размер: {len(df)} строк")
    print(f"Колонки: {list(df.columns)}")
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Визуализация: {filename}', fontsize=16)
    
    # Зависимость Intensity от Wave
    if 'Wave' in df.columns and 'Intensity' in df.columns:
        axes[0, 0].scatter(df['Wave'], df['Intensity'], s=1, alpha=0.5)
        axes[0, 0].set_xlabel('Wave')
        axes[0, 0].set_ylabel('Intensity')
        axes[0, 0].set_title('Спектр: Intensity vs Wave')
        axes[0, 0].grid(True, alpha=0.3)
    
    # Распределение Intensity
    if 'Intensity' in df.columns:
        axes[0, 1].hist(df['Intensity'], bins=50, edgecolor='black', alpha=0.7)
        axes[0, 1].set_xlabel('Intensity')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].set_title('Распределение Intensity')
        axes[0, 1].grid(True, alpha=0.3)
    
    # 3D scatter (X, Y, Intensity):
    if all(col in df.columns for col in ['X', 'Y', 'Intensity']):
        scatter = axes[1, 0].scatter(df['X'], df['Y'], 
                                     c=df['Intensity'], 
                                     cmap='viridis', 
                                     s=10, 
                                     alpha=0.6)
        axes[1, 0].set_xlabel('X')
        axes[1, 0].set_ylabel('Y')
        axes[1, 0].set_title('Пространственное распределение (Intensity)')
        plt.colorbar(scatter, ax=axes[1, 0])
        axes[1, 0].grid(True, alpha=0.3)
    
    # Распределение по категориям
    if 'cat' in df.columns:
        cat_counts = df['cat'].value_counts()
        axes[1, 1].bar(cat_counts.index, cat_counts.values, alpha=0.7)
        axes[1, 1].set_xlabel('Category')
        axes[1, 1].set_ylabel('Count')
        axes[1, 1].set_title('Распределение по категориям')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.show()
    
    # Показываем статистику
    print("\nСтатистика:")
    print(df.describe())

print('Пример:')
visualize_file('./data/control/mk1/cortex_control_1group_633nm_center1500_obj100_power100_1s_5acc_map35x15_step2_place4_1.txt')
