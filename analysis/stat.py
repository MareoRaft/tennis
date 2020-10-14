STAT_TO_COL_NAME = {
  'aces': 'isAce',
  'points-won': 'isPt',
}

def player_to_stat(df, stat, limit):
  ''' Given the point dataframe, output a [(player,num_stat),...] ranking. '''
  # Currently aiming to support 'aces' and 'points-won'
  agg_col = STAT_TO_COL_NAME[stat]
  # 'sql' query
  series_player_to_stat = df.groupby(['playerPtWinner'], as_index=True).agg({agg_col: 'sum'})[agg_col]
  top_player_to_stat = series_player_to_stat.nlargest(limit)
  # output
  list_player_to_stat = [(index,value) for index,value in top_player_to_stat.iteritems()]
  return list_player_to_stat
