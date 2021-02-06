import React, {useState} from 'react'
import classNames from 'classnames'

import classes from './PlayerRank.module.css'
import PlayerRankChart from '../PlayerRankChart'
import PlayerRankControls from '../PlayerRankControls'
import gc from '../../global-constants'
import env from '../../env'


function PlayerRank() {
  // init vars
	// set state
  const [gender, setGender] = useState(gc.DEFAULT_GENDER)
  const [stat, setStat] = useState(gc.DEFAULT_STAT)
  const [normalization, setNormalization] = useState(gc.DEFAULT_NORMALIZATION)
  const [reverse, setReverse] = useState(gc.DEFAULT_REVERSE)
  const [filter, setFilter] = useState(gc.DEFAULT_FILTER)
  const [limit, setLimit] = useState(gc.DEFAULT_LIMIT)
  const [data, setData] = useState([{category:'', value:0}])
  // create handlers
  const handleChangeGender = (event) => {
    setGender(event.target.value)
  }
  const handleChangeStat = (event) => {
    setStat(event.target.value)
  }
  const handleChangeNormalization = (event) => {
    setNormalization(event.target.value)
  }
  const handleChangeFilter = (event) => {
    setFilter(event.target.value)
  }
  const handleChangeReverse = (event) => {
    setReverse(event.target.value)
  }
  const handleChangeLimit = (event) => {
    setLimit(event.target.value)
  }
  const fetchData = React.useCallback(async () => {
    // update data
    const url = new URL(`${env.REACT_APP_BACKEND_URL}/data`)
    console.log(url)
    const params = {gender, stat, normalization, reverse, limit}
    url.search = new URLSearchParams(params).toString()
    const response = await fetch(url)
    const new_data = await response.json()
    setData(new_data)
  }, [gender, stat, normalization, reverse, limit, setData])
  // effects
  React.useEffect(() => {
    // run this immediately after rendering
    fetchData()
  }, [fetchData])
  // return rendered stuff
	return (
    <>
      <div className={classNames(classes.split, classes.left)}>
        <PlayerRankChart {...{
          gender,
          stat,
          normalization,
          filter,
          reverse,
          data,
        }}/>
      </div>
      <div className={classNames(classes.split, classes.right)}>
        <PlayerRankControls {...{
          gender,
          onChangeGender: handleChangeGender,
          stat,
          onChangeStat: handleChangeStat,
          normalization,
          onChangeNormalization: handleChangeNormalization,
          filter,
          onChangeFilter: handleChangeFilter,
          reverse,
          onChangeReverse: handleChangeReverse,
          limit,
          onChangeLimit: handleChangeLimit,
          onSubmit: fetchData,
        }}/>
      </div>
    </>
	);
}

export default PlayerRank;
