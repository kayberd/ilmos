import React, {useState} from 'react';

import Button from '../../components/Button';
import SeatIDView from '../../components/SeatIDView';
import {Image, StyleSheet, View} from 'react-native';
import Timer from './Timer';
import {
  ButtonText,
  DeskStatus,
  MAX_BREAK_MIN,
  Networking,
  REQUEST_HEADER,
} from '../../utils/constants';

const StudyView = ({
  seatId,
  startTime,
  breakTime,
  navigation,
  seatStatus,
  setIsSessionActive,
}) => {
  const [timerValue, setTimerValue] = useState(0);

  var hoursDifference = Math.floor(timerValue / 1000 / 60 / 60);

  var minutesDifference = Math.floor(
    (timerValue - hoursDifference * 1000 * 60 * 60) / 1000 / 60,
  );

  var secondsDifference = Math.floor(
    (timerValue -
      hoursDifference * 1000 * 60 * 60 -
      minutesDifference * 1000 * 60) /
      1000,
  );

  setTimeout(() => {
    const currTime = new Date().getTime();
    const timerValueByStatus =
      seatStatus === DeskStatus.TAKEN
        ? currTime - startTime
        : breakTime + MAX_BREAK_MIN - currTime;
    setTimerValue(timerValueByStatus); // update ~1000 milliseconds
  }, 1000);

  const releaseSeat = async () => {
    const userToken = global.USER_TOKEN;
    console.log('token when releasing seat: ', userToken);
    return await fetch(Networking.BASE_URL + Networking.RELEASE + seatId, {
      method: 'DELETE',
      headers: REQUEST_HEADER,
      body: JSON.stringify({
        user: userToken,
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('release seat: ', data.detail);
        setIsSessionActive(false);
      })
      .catch(error => {
        console.log('ERROR WHILE UPDATING release seat ' + error.message);
      });
  };

  const onEndSession = () => {
    releaseSeat();
    navigation.navigate('Dashboard');
  };

  const imageSource =
    seatStatus === DeskStatus.TAKEN
      ? require('../../../assets/working-padded.png')
      : require('../../../assets/break.png');

  const imageStyle =
    seatStatus === DeskStatus.TAKEN
      ? styles.takenImageStyle
      : styles.breakImageStyle;

  return (
    <View style={styles.studyView}>
      <View style={styles.topContainer}>
        <SeatIDView seatId={seatId} />
        <Timer
          hours={hoursDifference}
          minutes={minutesDifference}
          seconds={secondsDifference}
          seatStatus={seatStatus}
        />
      </View>
      <View style={styles.bottomContainer}>
        <Image source={imageSource} style={imageStyle} />
        <Button
          buttonStyle={styles.buttonStyle}
          buttonPress={onEndSession}
          buttonText={ButtonText.ENDSESSION}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  studyView: {
    width: '95%',
    alignItems: 'center',
    justifyContent: 'space-evenly',
    height: '100%',
  },
  takenImageStyle: {
    width: '90%',
    height: '60%',
    borderRadius: 10,
  },
  breakImageStyle: {
    width: '90%',
    height: '60%',
    borderRadius: 10,
  },
  topContainer: {
    height: '30%',
    justifyContent: 'flex-start',
  },
  bottomContainer: {
    width: '100%',
    height: '70%',
    justifyContent: 'space-evenly',
    alignItems: 'center',
  },
  buttonStyle: {
    backgroundColor: '#DD241F',
    borderRadius: 6,
    width: '75%',
    alignItems: 'center',
    justifyContent: 'center',
    height: '13%',
  },
});

export default StudyView;
