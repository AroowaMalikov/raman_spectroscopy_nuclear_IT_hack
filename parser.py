def parsing_data(dir_1, dir_2):
    names_columns = ['X', 'Y', 'Wave', 'Intensity', 'cat', 'feature_1', 'feature_2', 'feature_3',  'side']
    data = pd.DataFrame(columns=names_columns)
    names = os.listdir(f'data/{dir_1}/{dir_2}')
    number = 1

    for dir_3 in names[:]:
        print(dir_3)
        
        with open(f'data/{dir_1}/{dir_2}/{dir_3}', "r") as f:
            tqd = []
            f = f.readlines()
            for el in f[1:]:
                el = el.split()
                side = None
                for i in dir_3.split('_'):
                    if 'center' in i:
                        feature_2 = i
                    if 'cortex' in i or 'striatum' in i or 'cerebellum' in i:
                        feature_3 = i
                    if 'right' in i or 'left' in i:
                        side = i
                el.extend([dir_1, dir_2, feature_2, feature_3, side])
                tqd.append(el)
            data = pd.concat([data, pd.DataFrame(tqd, columns=names_columns)], axis=0)
    return data
