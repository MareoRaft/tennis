import pandas as pd
import ediblepickle

import data_ingestion.converters as convert
from data_ingestion import clean_csv

# DATAFRAME
def csv_to_df(file_path, col_names, col_types, col_converters, num_rows):
  df = pd.read_csv(file_path,
    encoding='utf_8',
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
  def get_player_serving(row):
    ''' Compute the id of the player who is serving. '''
    if row['Svr'] == 1:
      return row['player1']
    elif row['Svr'] == 2:
      return row['player2']
    else:
      raise ValueError(f"unknown Svr (server) '{row['Svr']}'")
  df['playerServing'] = df.apply(get_player_serving, axis=1)
  def get_point_winning_player(row):
    ''' Compute the id of the player who is serving. '''
    if row['PtWinner'] == 1:
      return row['player1']
    elif row['PtWinner'] == 2:
      return row['player2']
    elif row['PtWinner'] == 0:
      # point was a let, point was interupted, or data was missing
      return None
    else:
      raise ValueError(f"unknown PtWinner (point winner) '{row['PtWinner']}'")
  df['playerPtWinner'] = df.apply(get_point_winning_player, axis=1)
  def is_point(row):
    # Every row represents 1 point, of course
    return 1
  df['isPt'] = df.apply(is_point, axis=1)
  return df

@ediblepickle.checkpoint(key='init_dataframe.ediblepickle', work_dir='./cache', refresh=False)
def init_dataframe(file_path, num_rows):
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
    'PtWinner',
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
    'PtWinner': convert.player_num,
    'GmW': convert.player_num,
    'SetW': convert.player_num,
  }
  # remove any non-UTF-8 characters from the file
  clean_csv.remove_non_utf_8_chars(file_path)
  clean_file_path = clean_csv.get_output_file_path(file_path)
  # init the df from the cleaned file
  df = csv_to_df(clean_file_path, col_names, col_types, col_converters, num_rows)
  return df
