import React, { Component } from 'react';
import UserDisplay from './presenter';
import PropTypes from 'prop-types';
// const Container = props => <UserDisplay {...props} />;

class Container extends Component {
	static propTypes = {
		handleClick: PropTypes.func.isRequired,
	};
	render() {
		return <UserDisplay {...this.props} />;
	}
}

export default Container;
