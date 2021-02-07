import React from 'react'
import {
  FormControl, InputLabel, Select, MenuItem,
} from '@material-ui/core'
import {ExpandMore} from '@material-ui/icons'
import {makeStyles} from '@material-ui/core/styles'
import _ from 'lodash'

const useStyles = makeStyles((theme) => ({
    root: {
       borderBottom: '1px solid white',
    },
        '&:before': {
            borderColor: 'blue',
        },
        '&:after': {
            borderColor: 'orange',
        },

    icon: {
        fill: 'red',
    },

      formControl: {
    color: 'green',
    margin: theme.spacing(1),
    minWidth: 120,
    backgroundColor: 'yellow',
  },
  selectEmpty: {
    color: 'yellow',
    marginTop: theme.spacing(2),
    backgroundColor: 'cyan',
  },
  color: 'cyan',
  default: {
    color: 'cyan',
    backgroundColor: 'cyan',
  },
}))

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
  const classes = useStyles();
  return (
    <>
      <FormControl variant="filled" className={classes.formControl}>
        {/*<InputLabel id="demo-simple-select-filled-label">{props.label}</InputLabel>*/}
        <Select
          labelId="demo-simple-select-filled-label"
          id="demo-simple-select-filled"
          value={props.value}
          onChange={props.onChange}
        >
          {renderMenuItems(props.values)}
        </Select>
      </FormControl>
    </>
  );
}

export default MinimalSelect;
