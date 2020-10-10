import pandas as pd

import data_ingestion_converters as convert

# DATAFRAME
def csv_to_df(file_path, col_names, col_types, col_converters, num_rows):
  df = pd.read_csv(file_path,
    # encoding='utf_8', # leaving this blank allows pandas to tolerate non-utf-8 characters
    delimiter=',',
    header='infer', # read col names from file itself
    names=None, # since 'infer' is used above
    usecols=col_names,
    dtype=col_types,
    converters=col_converters,
    true_values=['TRUE'],
    false_values=['FALSE'],
    skipinitialspace=True,
    nrows=num_rows,
  )
  # create more columns
  def id_to_info(id_):
    date, gender, location, _, player1, player2 = id_.split('-')
    return [date, gender, location, _, player1, player2]
  df['player1'] = [
    id_to_info(id_)[4] for id_ in df['match_id']
  ]
  df['player2'] = [
    id_to_info(id_)[5] for id_ in df['match_id']
  ]
  return df

def init_dataframes(file_path, num_rows):
  """ Takes in file path and creates dataframe with only the info we want. """
  # import data
  # col names we need, (subset of col_names_full)
  col_names = [
    'match_id',
    'Svr', # server player number (1 or 2)
    'Ret', # returner player number
    'Serving', # server's initials
    'Pts', # the current point score
    'isAce',
    'isDouble',
    'isSvrWinner', # did server win the point
    'GmW', # game winner player number.  0 means that it's not a game ending point.
    'SetW', # set winner player number.  0 means that it's not a set ending point.
  ]
  # the data type of each column
  col_types = {
    'match_id': str,
    'Serving': str,
    'isAce': bool,
    'isSvrWinner': bool,
  }
  # the data cleaners for select columns
  # NONE_VALUES = ['', 'NON-', 'UNK']
  col_converters = {
    'Pts': convert.score,
    'isDouble': convert.double_fault,
    'Svr': convert.player_num,
    'Ret': convert.player_num,
    'GmW': convert.player_num,
    'SetW': convert.player_num,
  }
  df = csv_to_df(file_path, col_names, col_types, col_converters, num_rows)
  return df
