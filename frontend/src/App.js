import React from 'react'
import {createMuiTheme, ThemeProvider} from '@material-ui/core/styles'

import './App.css'
import PlayerRank from './components/PlayerRank'

const theme = createMuiTheme({
  palette: {
    type: 'dark',
  },
});


function App() {
  // set states
  // change handlers
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <header className="App-header">
          <PlayerRank/>
        </header>
      </div>
    </ThemeProvider>
  );
}

export default App;
