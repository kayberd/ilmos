import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {DeskStatus} from '../../utils/constants';
import {ClockIcon} from '../../utils/iconsIon';

const Timer = ({hours, minutes, seconds, seatStatus}) => {
  const timerFormatter = value => {
    return value / 10 >= 1 ? value.toString() : '0' + value;
  };
  return (
    <View
      style={
        seatStatus === DeskStatus.TAKEN
          ? styles.timerStudyContainer
          : styles.timerBreakContainer
      }>
      <ClockIcon size={40} />
      <View style={styles.timeBoxContainer}>
        <View style={styles.timeBox}>
          <Text style={styles.timerText}>{timerFormatter(hours)}</Text>
        </View>
        <Text style={styles.timerText}>:</Text>

        <View style={styles.timeBox}>
          <Text style={styles.timerText}>{timerFormatter(minutes)}</Text>
        </View>
        <Text style={styles.timerText}>:</Text>
        <View style={styles.timeBox}>
          <Text style={styles.timerText}>{timerFormatter(seconds)}</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  timerStudyContainer: {
    backgroundColor: '#a7e0a5',
    flexDirection: 'row',
    width: '100%',
    height: '40%',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    marginTop: '3%',
  },
  timeBoxContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '40%',
  },
  timeBox: {
    alignItems: 'center',
    justifyContent: 'space-between',
    borderRadius: 6,
  },
  timerText: {
    fontSize: 30,
    fontWeight: '400',
    color: '#000000',
  },
  timerBreakContainer: {
    backgroundColor: '#ffff7a',
    flexDirection: 'row',
    width: '100%',
    height: '40%',
    borderRadius: 8,
    justifyContent: 'space-evenly',
    alignItems: 'center',
    marginTop: '3%',
  },
});

export default Timer;
