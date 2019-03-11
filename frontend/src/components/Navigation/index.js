import { connect } from 'react-redux';
import Container from './container';
import { push } from 'react-router-redux'; //state를 변경 for routing 로케이션을 링크없이 변경
const mapDispatchToProps = (dispatch, ownProps) => {
	return {
		goToSearch: searchTerm => {
			dispatch(push(`/search/${searchTerm}`));
		},
	};
};
export default connect(
	null,
	mapDispatchToProps
)(Container);
