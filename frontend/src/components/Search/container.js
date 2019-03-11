import React, { Component } from 'react';
import Search from './presenter';
import PropTypes from 'prop-types';

class Container extends Component {
	state = {
		loading: true,
	};
	static propTypes = {
		searchByTerm: PropTypes.func.isRequired,
		userList: PropTypes.array,
		imageList: PropTypes.array,
	};
	componentDidMount() {
		const { searchByTerm } = this.props;
		searchByTerm();
	}

	componentDidUpdate(prevProps, prevState) {
		const { searchByTerm } = this.props;
		if (prevProps.match.params !== this.props.match.params) {
			searchByTerm();
		}
	}

	componentWillReceiveProps(nextProps) {
		// const { searchByTerm, pathname } = this.props;
		if (nextProps.userList && nextProps.imageList) {
			this.setState({
				loading: false,
			});
		}

		// if (nextProps.pathname !== pathname) {
		// 	searchByTerm();
		// }
	}

	render() {
		const { userList, imageList } = this.props;
		return <Search {...this.state} userList={userList} imageList={imageList} />;
	}
}
export default Container;
