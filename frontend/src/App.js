import React from 'react'
// import {createMuiTheme, ThemeProvider} from '@material-ui/core/styles'

import './App.css'
import PlayerRank from './components/PlayerRank'

// for now we'll stick with the default theme
// const theme = createMuiTheme({
//   palette: {
//     primary: {
//       main: '#00ff00',
//     },
//     secondary: {
//       main: '#4fc3f7',
//     },
//   },
// })

function App() {
  // set states
  // change handlers
  return (
    // <ThemeProvider theme={theme}>
      <div className="App">
        <header className="App-header">
          <PlayerRank/>
        </header>
      </div>
    // </ThemeProvider>
  );
}

export default App;
