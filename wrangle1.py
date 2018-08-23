# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 14:48:41 2018

@author: Artem Belopolsky
"""

# Import modules
import pandas as pd
import numpy as np

# Create a dataframe
raw_data = {'first_name': ['Jason', 'Molly', 'Helen', 'Laura', 'Katja'],
        'nationality': ['USA', 'USA', 'France', 'Netherlands', 'Russia'],
        'age': [42, 52, 36, 24, 70]}
df = pd.DataFrame(raw_data, columns = ['first_name', 'nationality', 'age'])

print df



def label(first, second):

    if first == 'Jason' and second =='USA':
        num = 1
    elif first == 'Helen' and second == 'France':
        num = 2
    else: num = 0

    return num

df['label'] = df.apply(lambda row: label(row['first_name'], row['nationality']), axis=1)

print df



