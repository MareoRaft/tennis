import React from 'react';

const UserInput = props => {
	return (
		<div className="UserInput">
			<textarea
				onChange={props.onChange}
				value={props.content}
			>
			</textarea>
			<div>
				length: {props.content.length}
			</div>
		</div>
	);
};

export default UserInput;
