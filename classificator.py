import pandas as pd
import os
from parser import parsing_data

dirs_2 = {
    'control': ['mk1', 'mk2a', 'mk2b', 'mk3'],
    'endo': ['mend1', 'mend2a', 'mend2b', 'mend3'],
    'exo': ['mexo1', 'mexo2a', 'mexo2b', 'mexo3']
}

os.makedirs('temp_chunks', exist_ok=True)
chunk_files = []

for dir_1, sub_dirs in dirs_2.items():
    for dir_2 in sub_dirs:
        print(f"Обрабатываю: {dir_1} / {dir_2}")

        df_chunk = parsing_data(dir_1, dir_2)

        filename = f'temp_chunks/{dir_1}_{dir_2}.csv'
        df_chunk.to_csv(filename, index=False)
        chunk_files.append(filename)

        del df_chunk

df_list = [pd.read_csv(f) for f in chunk_files]
df = pd.concat(df_list, ignore_index=True)

df.to_csv('full_dataset.csv', index=False)
print("0")
