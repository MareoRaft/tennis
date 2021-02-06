import React, {useState} from 'react'
import {
  Button,
  IconButton,
} from '@material-ui/core'

import classes from './PlayerRankControls.module.css'
import MinimalSelect from '../MinimalSelect'
import Overlay from '../Overlay'
import gc from '../../global-constants'
import constants from './constants'
import i from './traditional-i.png'


function PlayerRankControls(props) {
	// set state
  const [isOverlayDisplayed, setIsOverlayDisplayed] = useState(false)
  // create handlers
  const handleCloseOverlay = () => {
    setIsOverlayDisplayed(false)
  }
  const handleOpenOverlay = () => {
    setIsOverlayDisplayed(true)
  }
  // return rendered stuff
	return (
    <>
      <Overlay {...{
        showOverlay: isOverlayDisplayed,
        onClose: handleCloseOverlay,
        title: 'Normalization',
        sectionDict: constants.normalization,
      }}/>
      <div className={classes.controlTitle}>
        Stat
      </div>
      <MinimalSelect {...{
        onChange: props.onChangeStat,
        value: props.stat,
        values: gc.STAT_TO_DISPLAY_NAME,
      }}/>
      <div className={classes.controlTitle}>
        Normalization
        <IconButton {...{
          'aria-label': 'info',
          color: 'inherit',
          size: 'small',
          onClick: handleOpenOverlay,
        }}>
          <img src={i} alt='info' height='15px' className={classes.infoImage}/>
        </IconButton>
      </div>
      <MinimalSelect {...{
        onChange: props.onChangeNormalization,
        value: props.normalization,
        values: gc.NORMALIZATION_TO_DISPLAY_NAME,
      }}/>
      <div className={classes.controlTitle}>
        Filter Data
      </div>
      <MinimalSelect {...{
        onChange: props.onChangeFilter,
        value: props.filter,
        values: gc.FILTER_TO_DISPLAY_NAME,
      }}/>
      <div className={classes.controlTitle}>
        Reverse Results
      </div>
      <MinimalSelect {...{
        onChange: props.onChangeReverse,
        value: props.reverse,
        values: gc.REVERSE_VALUES,
      }}/>
      <div className={classes.controlTitle}>
        Number of Results
      </div>
      <MinimalSelect {...{
        onChange: props.onChangeLimit,
        value: props.limit,
        values: gc.LIMIT_VALUES,
      }}/>
      <div className={classes.controlTitle}>
        Gender
      </div>
      <MinimalSelect {...{
        onChange: props.onChangeGender,
        value: props.gender,
        values: gc.GENDER_TO_DISPLAY_NAME,
      }}/>
      <div className={classes.buttonTitle}>
        {/* this space intentionally blank */}
      </div>
      <Button {...{
        variant: 'contained',
        color: 'primary',
        size: 'large',
        disableElevation: true,
        onClick: props.onSubmit,
      }}>
        Crunch Data
      </Button>
    </>
	);
}

export default PlayerRankControls;
