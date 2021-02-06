import React from 'react'
import classNames from 'classnames'
import _ from 'lodash'
import {
  IconButton,
} from '@material-ui/core'
import {
  Close,
} from '@material-ui/icons'

import classes from './Overlay.module.css'


function Section(props) {
  return (
    <>
      <h3 {...{
        className: classes.sectionHeader,
      }}>
        {props.title}
      </h3>
      <p {...{
        className: classes.paragraph,
      }}>
        {props.description}
      </p>
    </>
  )
}

function Contents(props) {
  return <>
    <h2>{props.title}</h2>
    {_.map(props.sectionDict, (description, title) =>
      <Section {...{
        key: title,
        title,
        description,
      }}/>
    )}
  </>
}

function Overlay(props) {
  return <>
    <div {...{
      className: classNames({
        [classes.alertOverlay]: true,
        [classes.displayNone]: !props.showOverlay,
      }),
    }}>
      <div {...{
        className: classes.closeOverlay,
      }}>
        <IconButton {...{
          'aria-label': 'close',
          color: 'inherit',
          size: 'small',
          onClick: props.onClose,
        }}>
          <Close/>
        </IconButton>
      </div>
      <Contents {...{
        title: props.title,
        sectionDict: props.sectionDict,
      }}/>
    </div>
  </>
}

export default Overlay;
