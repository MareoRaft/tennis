import React, {useState} from 'react'

import Chart from '../Chart'


function Component() {
	// set state
  const [updateNum, setUpdateNum] = useState(1)
  // create handlers
  const handleClick = () => {
  	// Increment the update num, triggering the chart to update
  	setUpdateNum(updateNum + 1)
  }
  // return rendered stuff
	return (
    <Chart {...{
    	onClick: handleClick,
  		updateNum,
    }}/>
	);
}

export default Component;
