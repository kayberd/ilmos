import {DrawerActions} from '@react-navigation/native';
import React, {useEffect, useState} from 'react';

import {
  ActivityIndicator,
  DrawerLayoutAndroidBase,
  Image,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import {
  DeskStatus,
  Networking,
  REFRESH_PERIOD,
  REQUEST_HEADER,
} from '../../utils/constants';
import StudyView from './StudyView';

const ProfileScreen = ({navigation}) => {
  const [isSessionActive, setIsSessionActive] = useState();
  const [seatId, setSeatId] = useState();
  const [seatStatus, setSeatStatus] = useState();
  const [startTime, setStartTime] = useState();
  const [breakTime, setBreakTime] = useState();
  const [isLoading, setIsLoading] = useState(true);

  const getOccupation = async () => {
    const userToken = global.USER_TOKEN;
    //console.log('token in profile screen: ', userToken);
    return await fetch(
      Networking.BASE_URL + Networking.OCCUPATION + userToken,
      {
        method: 'GET',
        headers: REQUEST_HEADER,
      },
    )
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          console.log('---PROFILE SCREEN--- ', data.detail);
          setIsSessionActive(false);
          setIsLoading(false);
        } else {
          console.log('---PROFILE SCREEN--- Occupation info: ', data);

          const userStartTime = new Date(data.startTime).getTime();
          setStartTime(userStartTime);
          setSeatId(data.seat);
          setIsSessionActive(true);
          if (data.breakTime === null) {
            console.log('studying');
            setSeatStatus(DeskStatus.TAKEN);
          } else {
            console.log('in break');
            const userBreakTime = new Date(data.breakTime).getTime();
            setBreakTime(userBreakTime);
            console.log(data.breakTime);
            setSeatStatus(DeskStatus.BREAK);
          }
          setIsLoading(false);
        }
      })
      .catch(error => {
        console.log(
          '---PROFILE SCREEN--- ERROR WHILE UPDATING PEOPLEINQUEUE ' +
            error.message,
        );
      });
  };

  useEffect(() => {
    const interval = setInterval(() => {
      getOccupation();
    }, REFRESH_PERIOD);

    return () => {
      clearInterval(interval);
    };
  }, []);

  const didUserTookBreak = async () => {
    if (!isLoading && isSessionActive) {
      console.log(seatId);
      return await fetch(Networking.BASE_URL + Networking.SEAT + seatId, {
        method: 'GET',
        headers: REQUEST_HEADER,
      })
        .then(response => response.json())
        .then(data => {
          console.log('sa', data);
          setSeatStatus(data.status);
        })
        .catch(error => {
          console.log(
            '---PROFILE SCREEN--- ERROR WHILE UPDATING didUserTookBreak ' +
              error.message,
          );
        });
    } else {
      return -1;
    }
  };

  const ProfileScreenView = () => {
    if (isLoading) {
      return <ActivityIndicator animating={isLoading} size="large" />;
    } else {
      if (!isSessionActive) {
        const imageSource = require('../../../assets/no-session.png');
        return (
          <View style={styles.noSessionContainer}>
            <Image style={styles.noSession} source={imageSource} />
            <View style={styles.messageContainer}>
              <Text style={styles.messageStyle}>You should start to study</Text>
            </View>
          </View>
        );
      } else {
        return (
          <StudyView
            navigation={navigation}
            seatId={seatId}
            startTime={startTime}
            breakTime={breakTime}
            seatStatus={seatStatus}
            setIsSessionActive={setIsSessionActive}
          />
        );
      }
    }
  };

  return (
    <View style={styles.mainContainer}>
      <ProfileScreenView />
    </View>
  );
};

const styles = StyleSheet.create({
  mainContainer: {
    paddingVertical: '2%',
    alignItems: 'center',
    height: '100%',
    width: '100%',
    alignSelf: 'center',
    backgroundColor: '#FFFFFF',
    justifyContent: 'center',
  },
  noSessionContainer: {
    justifyContent: 'space-evenly',
    width: '90%',
    height: '70%',
  },
  messageContainer: {justifyContent: 'center', alignItems: 'center'},
  messageStyle: {fontSize: 22, fontWeight: '400', color: 'black'},
  noSession: {
    width: '90%',
    height: '70%',
  },
});

export default ProfileScreen;
