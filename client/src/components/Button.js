import React from 'react';
import {StyleSheet, Text} from 'react-native';
import {TouchableOpacity} from 'react-native';

const Button = ({buttonPress, buttonText, buttonStyle}) => {
  return (
    <TouchableOpacity
      onPress={buttonPress}
      style={buttonStyle ? buttonStyle : styles.button}>
      <Text style={styles.buttonText}>{buttonText}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#DD241F',
    borderRadius: 6,
    width: '75%',
    alignItems: 'center',
    justifyContent: 'center',
    height: '10%',
  },
  buttonText: {color: 'white', fontSize: 24},
});

export default Button;
