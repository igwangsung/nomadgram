import React, { Component } from 'react';
import Navigation from './presenter';
import PropTypes from 'prop-types';
class Container extends Component {
	state = {
		term: '',
	};
	static propTypes = {
		goToSearch: PropTypes.func.isRequired,
	};
	render() {
		return <Navigation value={this.state.term} onSubmit={this._onSubmit} onInputChange={this._onInputChange} />;
	}
	_onInputChange = event => {
		const {
			target: { value },
		} = event;
		this.setState({
			term: value,
		});
	};

	_onSubmit = event => {
		const { goToSearch } = this.props;
		const { term } = this.state;
		event.preventDefault();
		goToSearch(term);
		this.setState({
			term: '',
		});
	};
}

export default Container;
