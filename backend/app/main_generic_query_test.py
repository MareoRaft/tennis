from main_generic_query import main


def test_main():
  for stat in ('dblFault', 'ace', 'svcPtWin', 'ptWin'):
    assert len(main(gender='m', stat=stat, normalization='percent', reverse=False, limit=3, verbose=True)) == 3

def test_main_time_decay():
  for stat in ('dblFault', 'ace', 'svcPtWin', 'ptWin'):
    assert len(main(gender='m', stat='ptWin', normalization='time-decay', reverse=False, limit=3, verbose=True)) == 3
