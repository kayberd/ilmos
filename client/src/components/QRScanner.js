import React from 'react';
import {occupySeat} from '../utils/utils';
import {Alert, AsyncStorage, Image, StyleSheet} from 'react-native';
import {IlmosColors, QRResponseTexts} from '../utils/constants';
import QRCodeScanner from 'react-native-qrcode-scanner';

const QRScanner = ({navigation}) => {
  const responseHandler = response => {
    console.log(response.detail);
    if (response.detail === QRResponseTexts.OCCUPY_SUCCESS) {
      successHandler();
    } else if (response.detail === QRResponseTexts.SEAT_NOT_EMPTY) {
      seatTakenHandler();
    } else {
      undefinedResponseHandler();
    }
  };
  const successHandler = () => {
    navigation.navigate('Profile', {navigation: navigation});
  };
  const seatTakenHandler = () => {
    Alert.alert('Fail', 'Heyy!! There is somebody!!', [
      {text: 'OK', onPress: () => navigation.navigate('Dashboard')},
    ]);
  };
  const undefinedResponseHandler = (e) => {
    Alert.alert('Fail', 'Undefined Response Handler Error: ' + e, [
      {text: 'OK', onPress: () => navigation.navigate('Dashboard')},
    ]);
  };

  const readQr = e => {
    console.log(e);
    occupySeat(e.data)
      .then(json => {
        responseHandler(json);
      })
      .catch(e => console.log('Cant occupied seat Err:' + e));
  };

  const customMarker = () => {
    return (
      <Image
        style={styles.qrFrame}
        source={require('../../assets/qr-code.webp')}
      />
    );
  };

  return (
    <QRCodeScanner
      onRead={readQr}
      vibrate={true}
      fadeIn={true}
      reactivate={true}
      reactivateTimeout={3000}
      cameraProps={{captureAudio: false}}
      cameraContainerStyle={styles.cameraContainerStyle}
      cameraStyle={styles.cameraStyle}
      showMarker={true}
      customMarker={customMarker()}
      markerStyle={styles.marker}
    />
  );
};

const styles = StyleSheet.create({
  marker: {
    borderColor: 'white',
    height: '50%',
    width: '50%',
  },
  qrFrame: {
    tintColor: 'white',
  },
  cameraContainerStyle: {
    width: '100%',
    height: '100%',
    borderColor: IlmosColors.RED,
    alignSelf: 'center',
    borderStyle: 'solid',
    borderRadius: 10,
  },
  cameraStyle: {
    width: '100%',
    height: '100%',
    alignSelf: 'center',
    borderStyle: 'solid',
  },
});

export default QRScanner;
