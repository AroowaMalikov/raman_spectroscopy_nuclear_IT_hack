import pandas as pd
import os
import matplotlib.pyplot as plt
import random


def visualize_random_spectrum(filename, save_path=None):
    """
    Визуализирует случайный спектр из файла.
    
    Параметры:
    filename: путь к файлу
    save_path: путь для сохранения графика (если None, сохраняется автоматически)
    """
    # Проверка существования файла:
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return
    
    # Загрузка данных
    if filename.endswith('.txt'):
        names_columns = ['X', 'Y', 'Wave', 'Intensity', 'cat', 'feature_1', 'feature_2', 'feature_3', 'side']
        df = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=names_columns)
    else:
        df = pd.read_csv(filename)
        
    print(f"\nЗагружен файл: {filename}")
    print(f"Всего строк: {len(df)}")
    
    # === ВЫДЕЛЯЕМ ОТДЕЛЬНЫЕ СПЕКТРЫ ===
    # Один спектр = все измерения с одинаковыми координатами (X, Y)
    df['spectrum_id'] = df['X'].astype(str) + '_' + df['Y'].astype(str)
    
    unique_spectra = df['spectrum_id'].unique()
    total_spectra = len(unique_spectra)
    print(f"Найдено спектров: {total_spectra}")
    
    # === ВЫБИРАЕМ СЛУЧАЙНЫЙ СПЕКТР ===
    random_index = random.randint(0, total_spectra - 1)
    selected_id = unique_spectra[random_index]
    
    # Получаем данные выбранного спектра
    spectrum_df = df[df['spectrum_id'] == selected_id].sort_values('Wave')
    
    print(f"\nВыбран случайный спектр #{random_index + 1} из {total_spectra}")
    print(f"Координаты: {selected_id}")
    print(f"Точек в спектре: {len(spectrum_df)}")
    
    # === ГРАФИК ===
    plt.figure(figsize=(10, 6))
    plt.plot(spectrum_df['Wave'], spectrum_df['Intensity'], 
             color='blue', linewidth=0.8)
    
    plt.xlabel('Raman shift / cm⁻¹', fontsize=11)
    plt.ylabel('Counts', fontsize=11)
    plt.title(f'Случайный спектр (#{random_index + 1})\nКоординаты: {selected_id}', fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.xlim(950, 2000)
    
    plt.tight_layout()
    
    # Сохранение
    if save_path:
        output_path = save_path
    else:
        base_name = os.path.basename(filename).rsplit('.', 1)[0]
        output_path = f'random_spectrum_{base_name}.png'
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nГрафик сохранён: {output_path}")
    plt.close()
    
    # Статистика
    print(f"\nСтатистика интенсивности:")
    print(f"  Мин: {spectrum_df['Intensity'].min():.0f}")
    print(f"  Макс: {spectrum_df['Intensity'].max():.0f}")
    print(f"  Среднее: {spectrum_df['Intensity'].mean():.0f}")


# ===== 10 ПОСЛЕДОВАТЕЛЬНЫХ ВЫЗОВОВ =====
print('=' * 60)
print('Генерация 10 случайных спектров')
print('=' * 60)

file_path = './data/exo/mexo1/cortex_exo_1group_633nm_center1500_obj100_power100_1s_5acc_map35x15_step2_place4_1.txt'

# Вызов 1
print(f"\n{'='*60}")
print("ВЫЗОВ 1")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_1.png')

# Вызов 2
print(f"\n{'='*60}")
print("ВЫЗОВ 2")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_2.png')

# Вызов 3
print(f"\n{'='*60}")
print("ВЫЗОВ 3")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_3.png')

# Вызов 4
print(f"\n{'='*60}")
print("ВЫЗОВ 4")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_4.png')

# Вызов 5
print(f"\n{'='*60}")
print("ВЫЗОВ 5")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_5.png')

# Вызов 6
print(f"\n{'='*60}")
print("ВЫЗОВ 6")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_6.png')

# Вызов 7
print(f"\n{'='*60}")
print("ВЫЗОВ 7")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_7.png')

# Вызов 8
print(f"\n{'='*60}")
print("ВЫЗОВ 8")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_8.png')

# Вызов 9
print(f"\n{'='*60}")
print("ВЫЗОВ 9")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_9.png')

# Вызов 10
print(f"\n{'='*60}")
print("ВЫЗОВ 10")
print('='*60)
visualize_random_spectrum(file_path, save_path='spectrum_10.png')

print(f"\n{'='*60}")
print("ГОТОВО! Создано 10 файлов: spectrum_1.png ... spectrum_10.png")
print('='*60)