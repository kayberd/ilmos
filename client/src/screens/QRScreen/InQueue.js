import React from "react";
import Button from '../../components/Button';
import {ButtonText} from '../../utils/constants';
import { Text, View } from "react-native";
import { StyleSheet } from "react-native";
const InQueue = ({navigation, queueIndex, parentCallback}) => {
  const onPressLeave = () => {
    parentCallback();
  };

  console.log('-----IN QUEUE RENDERED------');
  console.log('queue number: ', queueIndex);

  return (
    <View style={styles.container}>
      <>
        <View style={styles.textView}>
          <Text style={styles.boringText}>You are</Text>
          <Text style={styles.number}>{queueIndex + 1}</Text>
          <Text style={styles.boringText}> in the line</Text>
        </View>
        <Button
          buttonStyle={styles.buttonStyle}
          buttonText={ButtonText.LEAVE_QUEUE}
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
    backgroundColor: '#DD241F',
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
  number: {fontSize: 70, color: '#DD241F', fontWeight: '600'},
});

export default InQueue;
