import React from 'react'

import RadialBarChart from '../RadialBarChart'
import gc from '../../global-constants'

const cleanName = (name) => {
  return name.replace(/[_]/g, ' ')
}

const getTitle = (gender, stat, filter, normalization, reverse) => {
  const Top = (reverse === 'true') ? 'Bottom' : 'Top'
  const male = (gender === 'm') ? 'male' : 'female'
  const grassCourt = (filter === 'none') ? '': `${filter}-court`
  const percent = (normalization === 'count') ? '#' : '%'
  const aces = gc.STAT_TO_DISPLAY_NAME[stat]
  const normalization_and_stat = (stat === 'pagerank') ? aces : `${percent} ${aces}`
  const title = `${Top} ${male} ${grassCourt} players by ${normalization_and_stat}`
  return title
}

function PlayerRankChart(props) {
  // clean data a bit
  const data = props.data.map((datum) => {
    return {
      ...datum,
      'category': cleanName(datum.category),
    }
  })
  // return rendered stuff
	return (
    <RadialBarChart {...{
      onClick: props.fetchData,
  		data,
      title: getTitle(props.gender, props.stat, props.filter, props.normalization, props.reverse),
    }}/>
	);
}

export default PlayerRankChart;
