import { createStore, combineReducers, compose, applyMiddleware } from 'redux';
import thunk from 'redux-thunk'; //리액트앱과 스토어 사이를 연결해준다,리덕스 스토어로 액션을 보낼수있다
import { connectRouter, routerMiddleware } from 'connected-react-router';
import createHistory from 'history/createBrowserHistory'; // 해쉬 히스토리도 있고, 히스토리의 종류 다양한듯
import { composeWithDevTools } from 'redux-devtools-extension';
import user from 'redux/modules/user';
import photos from 'redux/modules/photos';
import { i18nState } from 'redux-i18n';

const env = process.env.NODE_ENV;
const history = createHistory();
const middlewares = [thunk, routerMiddleware(history)];

if (env === 'development') {
	const { logger } = require('redux-logger');
	middlewares.push(logger);
}

const reducer = combineReducers({
	user,
	photos,
	i18nState,
});

let store;
if (env === 'development') {
	store = initialState =>
		createStore(connectRouter(history)(reducer), composeWithDevTools(applyMiddleware(...middlewares)));
} else {
	store = initialState => createStore(connectRouter(history)(reducer), compose(applyMiddleware(...middlewares)));
}
export { history };
export default store();
