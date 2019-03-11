import React, { Component } from 'react';
import LoginForm from './presenter';
import PropTypes from 'prop-types';

class Container extends Component {
	state = {
		username: '',
		password: '',
	};
	static propTypes = {
		facebookLogin: PropTypes.func.isRequired,
		usernameLogin: PropTypes.func.isRequired,
	};
	render() {
		const { username, password } = this.state;
		return (
			<LoginForm
				handleInputChange={this._handleInputChange}
				handleSubmit={this._handleSubmit}
				handleFacebookLogin={this._handleFacebookLogin}
				usernameValue={username}
				passwordValue={password}
			/>
		);
	}
	//const name = event.target.value
	_handleInputChange = event => {
		const {
			target: { value, name },
		} = event;
		this.setState({
			[name]: value,
		});
	};

	_handleSubmit = event => {
		const { usernameLogin } = this.props;
		const { username, password } = this.state;
		event.preventDefault();
		usernameLogin(username, password);
		//redux action will be here
	};

	_handleFacebookLogin = response => {
		const { facebookLogin } = this.props;
		facebookLogin(response.accessToken);
	};
}

export default Container;
