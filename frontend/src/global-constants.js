const gc = {
  DEFAULT_GENDER: 'm', // 'm' 'w'
  DEFAULT_STAT: 'ace',
  DEFAULT_NORMALIZATION: 'percent',
  DEFAULT_FILTER: 'none',
  DEFAULT_REVERSE: 'false',
  DEFAULT_LIMIT: 5,
  GENDER_TO_DISPLAY_NAME: {
    'm': 'men',
    'w': 'women',
  },
  STAT_TO_DISPLAY_NAME: {
    'ace': 'aces',
    'ptWin': 'points won',
    'svcPtWin': 'service points won',
    'dblFault': 'double faults',
    'pagerank': 'The GOAT algorithm',
  },
  NORMALIZATION_TO_DISPLAY_NAME: {
    'count': 'raw count',
    'percent': 'percent',
    'time-decay': 'time decay',
  },
  FILTER_TO_DISPLAY_NAME: {
    'none': 'use all data',
    'hard': 'hard court only',
    'clay': 'clay only',
    'grass': 'grass only',
  },
  REVERSE_VALUES: ['true', 'false'],
  LIMIT_VALUES: [3, 5, 8, 14],
}

export default gc
