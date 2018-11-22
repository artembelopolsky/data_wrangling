# -*- coding: utf-8 -*-
"""
This is a collection of handy data wrangling functions and tricks using pandas
that I have been accumulating

All functions and tricks contain examples

@author: Artem Belopolsky
"""

#==============================================================================
# Load modules
#==============================================================================

import pandas as pd
import numpy as np
import time
import StringIO


#==============================================================================
# Create a dataframe
#==============================================================================

raw_data = {'first_name': ['Jason', 'Andrew', 'Helen', 'Laura', 'Katja'],
        'nationality': ['USA', 'USA', 'France', 'Netherlands', 'Russia'],
        'age': [42, 52, 36, 24, 70],
        'height': [180, 175, 200, 195, 199],
        'image1': 0, 'image2': 1, 'image3': 1, 'image4': 1}

data = pd.DataFrame(raw_data)
#data_tmp = data.copy() # copy dataframe for speed comparison below

print data
print '\n\n\n'


#==============================================================================
# Create a new column in a dataframe based on values in other columns
# METHOD 1
# Step1: Create a function to apply to each row of entries
# Step2: Apply this function to the entries using df.apply()
#==============================================================================
df = data.copy()
# Step1
def label(first, second):

    if first == 'Jason' and second =='USA':
        num = 1
    elif first == 'Helen' and second == 'France':
        num = 2
    else: num = 0

    return num

# Step 2

tick = time.time()
df['label'] = df.apply(lambda row: label(row['first_name'], row['nationality']), axis=1)
tock = time.time()
print 'time for df.apply method: ' + str(tock-tick)
print df
print '\n\n\n'
time_apply = tock-tick

#==============================================================================
# Create a new column in a dataframe based on values in other columns
# METHOD 2
# Using list comprehension
#==============================================================================

df = data.copy() # copy the original data

tic = time.time()

s = [1 if (x == 'Jason' and y == 'USA') else 2 if (x == 'Helen' and y == 'France') else 0 for x,y in zip(df.first_name, df.nationality)]

df['label'] = s
toc = time.time()
time_listcomp = tock-tick

print 'time for list comprehension method: ' + str(tock-tick)
print 'df.apply() is ' + str(time_listcomp/time_apply) + 'times faster than list comprehention'

#==============================================================================
# Create a long table by stacking selected columns
# adapted from @jezrael
#==============================================================================

def stack_columns(df, colnames_to_stack, new_colname1, new_colname2):
      """

      Parameters
      ----------

      df : pandas dataframe
      cols_to_stack : list of column names that need to be stacked together
      new_colname1 : string containing the name for all stacked columns
      new_colname2 : string containng the name for value in stacked columns

      Returns
      -------
      A dataframe with two new columns instead of the columns to be stacked
      """

      # Make a list of column names to keep
      keep_colnames = list(df.columns.drop(colnames_to_stack))
      # Stack selected columns
      df = df.set_index(keep_colnames).stack().reset_index()

      # Figure out the level of the new column
      name_col = 'level_' + str(len(keep_colnames))
      # Replace that name with own name
      df = df.rename(columns={0:new_colname2, name_col:new_colname1})


      return df


# List of column names to keep
cols_to_stack = ['image1', 'image2', 'image3', 'image4']
# Stack the columns
df = stack_columns(df, cols_to_stack, 'image', 'correct')

print df
print '\n\n\n'


#==============================================================================
# Sometimes a cell in a dataframe contains a list
# Expand such a list into separate columns
# adapted from @jezrael
#==============================================================================

def expand_list_to_cols(df, col_name):
  """

  Parameters
  ----------

  df : pandas dataframe
  col_name : string containing the column name with the list

  Returns
  -------
  A dataframe with two new columns instead of the columns to be stacked
  """

  # Make a list of all columns besides the column containing the list
  cols = df.columns[df.columns != col_name].tolist()
  # Creat a series from list and join it to the rest of the columns
  df = df[cols].join(df[col_name].apply(pd.Series))

  return df


# Create an example dataframe
df = pd.read_csv(StringIO.StringIO("""
id|name|fields
1|abc|[qq,ww,rr]
2|efg|[zz,xx,rr]

"""), sep='|')

# Turn a string into list
df.fields = df.fields.apply(lambda s: s[1:-1].split(','))
print df
print '\n'

# Expand list into columns
df = expand_list_to_cols(df,'fields')
print df
print '\n'


#==============================================================================
# Select the data based on items NOT in the list
# Can be handy for excluding multiple participants at once
#==============================================================================

df = data.copy()

df = df[~df.first_name.isin(['Jason','Helen'])]

print df


#==============================================================================
# Bin the data
#
#==============================================================================

def bin_data(df, col_name, custom_bins):
  """

  Parameters
  ----------

  df : pandas dataframe
  col_name : string containing the column name with the list

  Returns
  -------
  A dataframe with two new columns instead of the columns to be stacked
  """






  return df


raw_data = {'first_name': ['Jason', 'Andrew', 'Helen', 'Laura', 'Katja'],
        'nationality': ['USA', 'USA', 'France', 'Netherlands', 'Russia'],
        'age': [42, 52, 36, 24, 70],
        'height': [180, 175, 200, 195, 195],
        'image1': 0, 'image2': 1, 'image3': 1, 'image4': 1}

data = pd.DataFrame(raw_data)


# Set the time bins for one and two abnormalites
custom_bins = np.linspace(170, 200, 10)

data['time_bins'] = pd.cut(data.height, custom_bins)

fixcount = data.groupby([data.age, data.first_name, data.nationality, data.height, data.image1, data.image2, data.image3, data.time_bins]).size()

a = fixcount.reset_index()
a.rename(columns = {0:'fix_count'}, inplace=True)

a['proportion'] = a['fix_count'].div(a.groupby([a.age, a.first_name, a.nationality, a.height, a.image1, a.image2, a.image3, a.time_bins])['fix_count'].transform('sum'))
