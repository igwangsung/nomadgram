import React from 'react';
import styles from './styles.scss';
import Ionicons from 'react-ionicons';
import Loading from 'components/Loading';
import PropTypes from 'prop-types';
import UserDisplay from 'components/UserDisplay';

const UserList = props => (
	<div className={styles.container}>
		<div className={styles.box}>
			<header className={styles.header}>
				<h4 className={styles.title}>{props.title}</h4>
				<span onClick={props.closeLikes}>
					<Ionicons icon="md-close" fontSize="20px" color="black" />
				</span>
			</header>
			<div className={styles.content}>{props.loading ? <Loading /> : <RenderUsers list={props.userList} />}</div>
		</div>
	</div>
);

const RenderUsers = props => props.list.map(user => <UserDisplay horizontal={true} user={user} key={user.id} />);

RenderUsers.propTypes = {
	list: PropTypes.array,
};

UserList.propTypes = {
	title: PropTypes.string.isRequired,
	loading: PropTypes.bool.isRequired,
	users: PropTypes.array,
	userList: PropTypes.array,
	closeLikes: PropTypes.func.isRequired,
};

export default UserList;
