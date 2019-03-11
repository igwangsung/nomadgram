import Container from './container';
import { connect } from 'react-redux';
import { actionCreators as photoActions } from 'redux/modules/photos';

const mapDispatchToProps = (dispatch, ownProps) => {
	return {
		getFeed: () => {
			dispatch(photoActions.getFeed());
		},
	};
};
const mapStateToProps = (state, ownProps) => {
	const {
		photos: { feed },
	} = state;
	return {
		feed,
	};
};

export default connect(
	mapStateToProps,
	mapDispatchToProps
)(Container);
