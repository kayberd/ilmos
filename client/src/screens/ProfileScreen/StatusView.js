import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {DeskStatus, UserStatusText} from '../../utils/constants';
import {CoffeeIcon, GearsIcon} from '../../utils/icons';

const StatusView = ({seatStatus}) => {
  return (
    <View style={styles.statusView}>
      <View style={styles.statusContainer}>
        <View style={styles.statusIcon}>
          {seatStatus === DeskStatus.TAKEN ? <GearsIcon /> : <CoffeeIcon />}
        </View>
        <Text style={styles.statusText}>
          {seatStatus === DeskStatus.TAKEN
            ? UserStatusText.WORKING
            : UserStatusText.BREAK}
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  statusView: {
    backgroundColor: '#8bc8db',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    height: '20%',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-evenly',
    width: '80%',
  },
  statusText: {
    fontSize: 30,
    color: '#000000',
    fontWeight: '300',
  },
});

export default StatusView;
