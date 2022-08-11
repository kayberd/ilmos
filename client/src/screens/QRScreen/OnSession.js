import {Image, SafeAreaView, StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {QrScreenTexts} from '../../utils/constants';

const OnSession = () => {
  const imageSource = require('../../../assets/on-session.jpeg');
  return (
    <SafeAreaView style={styles.mainContainer}>
      <View style={styles.onSessionContainer}>
        <Image style={styles.onSession} source={imageSource} />
        <View style={styles.messageContainer}>
          <Text style={styles.messageStyle}>
            {' '}
            {QrScreenTexts.ON_SESSION_TEXT}
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  mainContainer: {
    alignItems: 'center',
    height: '100%',
    width: '100%',
    alignSelf: 'center',
    backgroundColor: '#FFFFFF',
    justifyContent: 'center',
  },
  onSessionContainer: {
    justifyContent: 'space-evenly',
    width: '90%',
    height: '70%',
  },
  messageContainer: {justifyContent: 'center', alignItems: 'center'},
  messageStyle: {fontSize: 22, fontWeight: '400', color: 'black'},
  onSession: {
    width: '90%',
    height: '70%',
    marginLeft: '6%',
  },
});
export default OnSession;
