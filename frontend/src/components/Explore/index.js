import Container from './container';
import { connect } from 'react-redux';
import { actionCreators as userActions } from 'redux/modules/user';

const mapDispatchToProps = (dispatch, ownProps) => {
	return {
		getExplore: () => {
			dispatch(userActions.getExplore());
		},
	};
};
const mapStateToProps = (state, ownProps) => {
	const {
		user: { userList },
	} = state;
	return {
		userList,
	};
};

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Container);
