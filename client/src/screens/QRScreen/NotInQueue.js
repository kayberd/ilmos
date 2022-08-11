import React, {useEffect, useState} from 'react';
import {ActivityIndicator, View, StyleSheet, Text} from 'react-native';
import Button from '../../components/Button';
import {ButtonText, Networking, REQUEST_HEADER} from '../../utils/constants';

const NotInQueue = ({navigation, peopleInQueue, parentCallback}) => {
  const onPressLeave = () => {
    parentCallback();
  };
  console.log('-----NOT IN QUEUE RENDERED------');
  console.log('queue number: ', peopleInQueue);

  return (
    <View style={styles.container}>
      <>
        <View style={styles.textView}>
          <Text style={styles.boringText}>
            There {peopleInQueue > 1 ? 'are' : 'is'}
          </Text>
          <Text style={styles.number}>{peopleInQueue}</Text>
          <Text style={styles.boringText}>people waiting</Text>
        </View>
        <Button
          buttonStyle={styles.buttonStyle}
          buttonText={ButtonText.ENTER_QUEUE}
          buttonPress={onPressLeave}
        />
      </>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: 'space-evenly',
    marginBottom: 35,
    alignItems: 'center',
    width: '80%',
  },
  buttonStyle: {
    backgroundColor: 'green',
    borderRadius: 6,
    height: '15%',
    width: '80%',
    alignItems: 'center',
    justifyContent: 'center',
  },
  textView: {
    height: '50%',
    width: '100%',
    justifyContent: 'space-evenly',
    alignItems: 'center',
  },
  boringText: {fontSize: 30, color: '#000000'},
  number: {fontSize: 75, color: '#DD241F', fontWeight: '600'},
});

export default NotInQueue;
