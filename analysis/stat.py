STAT_TO_GROUP_AGG_COL = {
  'aces': ('playerPtWinner', 'isAce'),
  'double-faults': ('playerPtLoser', 'isDouble'),
  'points-won': ('playerPtWinner', 'isPt'),
  'service-points-won': ('playerPtWinner', 'isSvrWinner'),
}

def player_to_stat(df, stat, limit):
  ''' Given the point dataframe, output a [(player,num_stat),...] ranking. '''
  # Currently aiming to support 'aces' and 'points-won'
  print(df.head())
  groupby_col = STAT_TO_GROUP_AGG_COL[stat][0]
  agg_col = STAT_TO_GROUP_AGG_COL[stat][1]
  # 'sql' query
  series_player_to_stat = df.groupby([groupby_col], as_index=True).agg({agg_col: 'sum'})[agg_col]
  top_player_to_stat = series_player_to_stat.nlargest(limit)
  # output
  list_player_to_stat = [(index,value) for index,value in top_player_to_stat.iteritems()]
  return list_player_to_stat
