import React from 'react'
import {
  FormControl, InputLabel, Select, MenuItem,
} from '@material-ui/core'
import {ExpandMore} from '@material-ui/icons'
import {makeStyles} from '@material-ui/core/styles'
import _ from 'lodash'

const useStyles = makeStyles((theme) => ({
  formControl: {
    minWidth: 160,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
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
        {/* If you want labels on the dropdown itself */}
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
