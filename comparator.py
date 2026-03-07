import pandas as pd
import os
import matplotlib.pyplot as plt
import random


def load_spectra_from_file(filename):
    """
    Загружает все отдельные спектры из файла.
    Возвращает словарь: {spectrum_id: DataFrame с колонками Wave, Intensity}
    """
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден!")
        return {}
    
    # Загрузка данных
    if filename.endswith('.txt'):
        names_columns = ['X', 'Y', 'Wave', 'Intensity', 'cat', 'feature_1', 'feature_2', 'feature_3', 'side']
        df = pd.read_csv(filename, sep=r'\s+', skiprows=1, names=names_columns)
    else:
        df = pd.read_csv(filename)
    
    # Группируем по координатам (X, Y) — это отдельные спектры
    df['spectrum_id'] = df['X'].astype(str) + '_' + df['Y'].astype(str)
    
    spectra = {}
    for spec_id in df['spectrum_id'].unique():
        spec_df = df[df['spectrum_id'] == spec_id][['Wave', 'Intensity']].sort_values('Wave')
        spectra[spec_id] = spec_df
    
    return spectra


def plot_single_spectrum(df_spec, title, save_path, color='blue'):
    """
    Сохраняет график одного спектра.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df_spec['Wave'], df_spec['Intensity'], color=color, linewidth=0.8)
    
    plt.xlabel('Raman shift / cm⁻¹', fontsize=11)
    plt.ylabel('Counts', fontsize=11)
    plt.title(title, fontsize=13)
    plt.grid(True, alpha=0.3)
    plt.xlim(950, 2000)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Сохранено: {save_path}")


def plot_comparison_spectrum(df_list, labels, colors, save_path):
    """
    Сохраняет сравнительный график нескольких спектров.
    """
    plt.figure(figsize=(12, 7))
    
    # Вертикальные оффсеты для наглядности
    offsets = [0, 15000, 30000]
    
    for i, (df_spec, label, color) in enumerate(zip(df_list, labels, colors)):
        intensity_offset = df_spec['Intensity'] + offsets[i]
        plt.plot(df_spec['Wave'], intensity_offset, color=color, linewidth=0.8, label=label)
    
    # Подписи пиков
    peaks = [1062, 1128, 1294, 1420, 1440]
    peak_labels = ['phospholipids', 'C-C', 'proteins', 'nucleic acids', 'lipids']
    
    for peak, plabel in zip(peaks, peak_labels):
        plt.axvline(x=peak, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        plt.text(peak, 50000, plabel, rotation=90, va='bottom', ha='center', 
                fontsize=8, bbox=dict(boxstyle='square', facecolor='white', edgecolor='gray', alpha=0.7))
    
    plt.xlabel('Raman shift / cm⁻¹', fontsize=12)
    plt.ylabel('Counts (offset for clarity)', fontsize=12)
    plt.title('Comparison: control vs endo vs exo (single random spectrum each)', fontsize=14)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(950, 2000)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Сохранено: {save_path}")


# ===== ОСНОВНАЯ ПРОГРАММА =====
print('=' * 70)
print('Визуализация случайных спектров (по одному из файла)')
print('=' * 70)

# Фиксируем seed для воспроизводимости (удалите для настоящей случайности)
random.seed(42)

# Конфигурация файлов и групп
files_config = [
    {
        'path': './data/endo/mend1/cortex_endo_1group_633nm_center1500_obj100_power100_1s_5acc_map35x15_step2_place1_1.txt',
        'label': 'endo (1 group)',
        'color': 'blue',
        'output_single': 'spectrum_endo.png'
    },
    {
        'path': './data/control/mk1/cortex_control_1group_633nm_center1500_obj100_power100_1s_5acc_map35x15_step2_place4_1.txt',
        'label': 'control (1 group)',
        'color': 'red',
        'output_single': 'spectrum_control.png'
    },
    {
        'path': './data/exo/mexo1/cortex_exo_1group_633nm_center1500_obj100_power100_1s_5acc_map35x15_step2_place4_1.txt',
        'label': 'exo (1 group)',
        'color': 'green',
        'output_single': 'spectrum_exo.png'
    }
]

spectra_dfs = []
labels = []
colors = []

# Обрабатываем каждый файл
for config in files_config:
    print(f"\n[Обработка] {config['label']}")
    print(f"  Файл: {config['path']}")
    
    # Загружаем спектры
    spectra = load_spectra_from_file(config['path'])
    if not spectra:
        print(f"  ✗ Не удалось загрузить спектры из {config['path']}")
        continue
    
    print(f"  Всего спектров в файле: {len(spectra)}")
    
    # Выбираем ОДИН случайный спектр
    selected_id = random.choice(list(spectra.keys()))
    df_spec = spectra[selected_id]
    
    # Фильтруем диапазон волн
    df_spec = df_spec[(df_spec['Wave'] >= 950) & (df_spec['Wave'] <= 2000)]
    
    print(f"  Выбран спектр: {selected_id} ({len(df_spec)} точек)")
    
    # Сохраняем отдельный график
    plot_single_spectrum(df_spec, f"Random spectrum: {config['label']}", 
                        config['output_single'], config['color'])
    
    # Сохраняем для сравнительного графика
    spectra_dfs.append(df_spec)
    labels.append(config['label'])
    colors.append(config['color'])

# Создаём сравнительный график (если все три файла обработаны)
if len(spectra_dfs) == 3:
    print(f"\n[Сравнение] Создаём общий график...")
    plot_comparison_spectrum(spectra_dfs, labels, colors, 'comparison_single_spectra.png')
else:
    print(f"\n[Внимание] Не все файлы обработаны, сравнительный график не создан")

print(f"\n{'=' * 70}")
print("ГОТОВО!")
print("Созданные файлы:")
print("  • spectrum_endo.png          — случайный спектр endo")
print("  • spectrum_control.png       — случайный спектр control") 
print("  • spectrum_exo.png           — случайный спектр exo")
print("  • comparison_single_spectra.png — сравнение всех трёх спектров")
print('=' * 70)