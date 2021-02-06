import React, {useState} from 'react'
import {FaAlignRight} from 'react-icons/fa'

import './Nav.css'

function Nav(props) {
  // set states
  const [isNavBarOpen, setIsNavBarOpen] = useState(true)
  // change handlers
  const handleToggleNav = () => {
    setIsNavBarOpen(!isNavBarOpen)
  }
  return (
    <div className="nav-bar">
      <button className="nav-button" onClick={handleToggleNav}>
        <FaAlignRight/>
      </button>
      <ul className={isNavBarOpen ? 'nav-links show-nav': 'nav-links'}>
        <li href='#'>Stock Ticker App</li>
        <li>
          <a
            className="App-link"
            href="https://github.com/MareoRaft/stock-backend-tdi"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </li>
        <li>
          <a
            className="App-link"
            href="https://www.thedataincubator.com/12day.html"
            target="_blank"
            rel="noopener noreferrer"
          >
            12-day
          </a>
        </li>
      </ul>
    </div>
  )
}

export default Nav;
