import React from 'react'
import PropTypes from 'prop-types'
import Iframe from 'react-iframe'

import './Iframe.css'



class Iframe2 extends React.Component {
	render() {
		return (
			<Iframe {...{
		        className: "iframe",
				url: this.props.url,
		        width: "620px",
		        height: "620px",
		        id: "myId",
		        display: "initial",
		        position: "relative",
			}}/>
        );
	}
}

const propTypes = {
	url: PropTypes.string.isRequired,
};

Iframe2.propTypes = propTypes;
export default Iframe2;
