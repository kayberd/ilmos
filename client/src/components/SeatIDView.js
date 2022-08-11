import React from 'react';
import {Image, Platform, StyleSheet, Text, View} from 'react-native';

const SeatIDView = ({seatId}) => {
  const userIconSource = require('../../assets/profile-screen-image.png');
  const userIconStyle = Platform.OS === 'ios' ? styles.profileImageIOS : styles.profileImage;
  return (
    <View style={styles.seatIdView}>
      <View style={styles.seatIdContainer}>
        <Image style={userIconStyle} source={userIconSource} />
        <View style={styles.seatIdTextContainer}>
          <Text style={styles.seatIdText}>Seat {seatId}</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  seatIdView: {
    backgroundColor: '#f7ba7b',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    borderRadius: 3,
    width: '100%',
    height: '40%',
  },
  seatIdTextContainer: {
    width: '40%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  seatIdContainer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    height: '100%',
    width: '100%',
    alignItems: 'center',
  },
  seatIdText: {
    fontSize: 30,
    fontWeight: '400',
    color: '#000000',
  },
  profileImage: {resizeMode: 'center', width: '15%', height: '50%'},
  profileImageIOS: { width: '10%', height: '52%'},
});

export default SeatIDView;
