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
import random


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

#print data
#print '\n\n\n'


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

# Step 2 Example

#tick = time.time()
#df['label'] = df.apply(lambda row: label(row['first_name'], row['nationality']), axis=1)
#tock = time.time()
#print 'time for df.apply method: ' + str(tock-tick)
#print df
#print '\n\n\n'
#time_apply = tock-tick

#==============================================================================
# Create a new column in a dataframe based on values in other columns
# METHOD 2
# Using list comprehension
#==============================================================================

df = data.copy() # copy the original data

tic = time.time()

s = [1 if (x == 'Jason' and y == 'USA') else 2 if (x == 'Helen' and y == 'France') else 0 for x,y in zip(df.first_name, df.nationality)]

# Example:
#df['label'] = s
#toc = time.time()
#time_listcomp = tock-tick

#print 'time for list comprehension method: ' + str(tock-tick)
#print 'df.apply() is ' + str(time_listcomp/time_apply) + 'times faster than list comprehention'

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

      Example
      -------
      # List of column names to keep
      cols_to_stack = ['image1', 'image2', 'image3', 'image4']
      # Stack the columns
      df = stack_columns(df, cols_to_stack, 'image', 'correct')

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

  Example
  -------

  # Create an example dataframe
  df = pd.read_csv(StringIO.StringIO("""
#  id|name|fields
#  1|abc|[qq,ww,rr]
#  2|efg|[zz,xx,rr]

  """), sep='|')

  # Turn a string into list
  df.fields = df.fields.apply(lambda s: s[1:-1].split(','))
  print df
  print '\n'

  # Expand list into columns
  df = expand_list_to_cols(df,'fields')
  print df
  print '\n'

  """

  # Make a list of all columns besides the column containing the list
  cols = df.columns[df.columns != col_name].tolist()
  # Creat a series from list and join it to the rest of the columns
  df = df[cols].join(df[col_name].apply(pd.Series))

  return df



#==============================================================================
# Select the data based on items NOT in the list
# Can be handy for excluding multiple participants at once
#==============================================================================

#df = data.copy()
#
#df = df[~df.first_name.isin(['Jason','Helen'])]
#
#print df


#==============================================================================
# Bin the data
#
#==============================================================================

def bin_data(df, in_col_name, out_col_name, bin_start, bin_stop, num_bins):
  """

  Parameters
  ----------

  df : pandas dataframe
  in_col_name : string containing the column name with a varible to bin
  out_col_name: string containing the column name with respective bin
  bin_start: the earliest time of all bins
  bin_end: the latest time of all bins
  num_bins: total number of bins

  Returns
  -------
  A dataframe with a new column containing the bins

  Example
  -------

  # Create a dataframe
  raw_data = {'latency': np.random.randint(100, 500, size=10),
                 'accuracy': np.random.randint(0,2,size=10),
                 }

  df = pd.DataFrame(raw_data)
  df = bin_data(df, 'latency', 'time_bins', bin_start=0, bin_stop=600, num_bins=6)
  df.accuracy.groupby([df.time_bins]).mean().plot()
  df.accuracy.groupby([df.time_bins]).mean()


  """

  custom_bins = np.linspace(bin_start, bin_stop, num_bins+1)
  df[out_col_name] = pd.cut(df[in_col_name], custom_bins)


  return df


