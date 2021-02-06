import React from 'react'
import { useMinimalSelectStyles } from '@mui-treasury/styles/select/minimal';
import {
  Select, MenuItem,
} from '@material-ui/core'
import {ExpandMore} from '@material-ui/icons'
import _ from 'lodash'

const renderMenuItems = (values) => {
  if (Array.isArray(values)) {
    return values.map((v) =>
      <MenuItem key={v} value={v}>{v}</MenuItem>
    )
  }
  else {
    return _.map(values, (v,k) =>
      <MenuItem key={k} value={k}>{v}</MenuItem>
    )
  }
}

const MinimalSelect = (props) => {
  const minimalSelectClasses = useMinimalSelectStyles()
  const iconComponent = (props) => {
    return (
      <ExpandMore className={props.className + ' ' + minimalSelectClasses.icon}/>
    )
  }
  // moves the menu below the select input
  const menuProps = {
    classes: {
      paper: minimalSelectClasses.paper,
      list: minimalSelectClasses.list,
    },
    anchorOrigin: {
      vertical: "bottom",
        horizontal: "left",
    },
    transformOrigin: {
      vertical: "top",
        horizontal: "left",
    },
    getContentAnchorEl: null,
  }
  return (
    <>
      <Select
        disableUnderline
        classes={{ root: minimalSelectClasses.select }}
        MenuProps={menuProps}
        IconComponent={iconComponent}
        value={props.value}
        onChange={props.onChange}
      >
        {renderMenuItems(props.values)}
      </Select>
    </>
  );
}

export default MinimalSelect;
