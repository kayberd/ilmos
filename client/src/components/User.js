import React from 'react';
import {StyleSheet} from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

import {DashboardColors} from '../utils/constants';

const User = ({seatStatus}) => {
  if (seatStatus) {
    switch (seatStatus) {
      case 'TAKEN':
        return (
          <Icon
            style={styles.icon}
            name="user"
            size={32}
            color={DashboardColors.TAKEN_COLOR}
          />
        );
      case 'VACANT':
        return (
          <Icon
            style={styles.icon}
            name="user"
            size={32}
            color={DashboardColors.VACANT_COLOR}
          />
        );
      case 'BREAK':
        return (
          <Icon
            style={styles.icon}
            name="user"
            size={32}
            color={DashboardColors.BREAK_COLOR}
          />
        );
      default:
        return <Icon style={styles.icon} name="user" size={32} color="black" />;
    }
  }
};

const styles = StyleSheet.create({
  icon: {marginHorizontal: 15, marginVertical: 3},
});

export default User;
