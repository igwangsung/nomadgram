import { connect } from 'react-redux';
import Container from './container';
import { actionCreators as userActions } from 'redux/modules/user';
//액션을 리듀서에게 디스패치하기
//리덕스 타이머에서 쓰인 mapDispatchToProps와는 다른 형태다 저거는 함수형태
const mapDispatchToProps = (dispatch, ownProps) => {
	return {
		facebookLogin: access_token => {
			//prop function이라함.
			dispatch(userActions.facebookLogin(access_token));
		},
		usernameLogin: (email, password) => {
			dispatch(userActions.usernameLogin(email, password));
		},
	};
};
export default connect(
	null,
	mapDispatchToProps
)(Container);
//first Argument is mapStateToProps
