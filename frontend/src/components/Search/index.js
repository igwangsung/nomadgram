import { connect } from 'react-redux';
import Container from './container';
import { actionCreators as userActions } from 'redux/modules/user';

const mapStateToProps = (state, ownProps) => {
	const {
		user: { userList, imageList },
		router: { location },
	} = state;
	return {
		userList,
		imageList,
		location,
	};
};
//라우터에서 props를 얻을수있음
const mapDispatchToProps = (dispatch, ownProps) => {
	const {
		match: {
			params: { searchTerm },
		},
	} = ownProps;
	return {
		searchByTerm: () => {
			dispatch(userActions.searchByTerm(searchTerm));
		},
	};
};

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Container);
