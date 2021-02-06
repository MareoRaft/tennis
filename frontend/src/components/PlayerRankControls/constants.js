import React from 'react'

import exponentialDecayImage from './exponential_function_half_to_x.png'


export default {
	normalization: {
		// 'raw count': <>This is merely the total number of points counted for the given stat.  For example, if the stat is "aces", then players will be ranked by the total number of aces they hit.</>,

    'percent': <>This is the percentage of points observed for the given stat.  For example, if the stat is "points won", then players will be ranked by the percentage of points they won.  That's (number points won) / (number points played).  For example, if the stat is "aces", then the value that players are ranked by is (number of aces) / (number of service points).  This is a good normalization for seeing who is the "best of all time" for a given stat.</>,

    'time decay': <>
      This is similar to percentage, but more recent points are weighted higher than points that happened a long time ago.  This is a great normalization for seeing who is the best player "today" per se.  We use a 1-year half-life exponential decay function, so that a point that occurred 1 year ago is only worth half as much as a point that happened today.
      <br/><br/>
      <img {...{
        src: exponentialDecayImage,
        alt: '1-year half-life exponential decay',
        height: '200px',
        style: {filter: 'hue-rotate(135deg)'},
      }}/>
    </>,
	},
}


/*
Please note that <strong>count</strong> normalization is very unreliable because more data has been recorded for more popular players.  So Roger Federer will have a higher count for aces even though other players have hit more aces than him.
*/
