import pandas as pd
import os
from parser import parsing_data


dirs_1 = ['control', 'endo', 'exo']

dirs_2 ={
    'control': ['mk1', 'mk2a', 'mk2b', 'mk3'],
    'endo': ['mend1', 'mend2a', 'mend2b', 'mend3'],
    'exo': ['mexo1', 'mexo2a', 'mexo2b', 'mexo3']
}


df = parsing_data('control', 'mk1')

df.head()