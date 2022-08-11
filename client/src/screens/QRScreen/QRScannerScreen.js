import React, {useEffect, useState} from 'react';
import {
  Networking,
  REFRESH_PERIOD,
  REQUEST_HEADER,
} from '../../utils/constants';
import QueueScreen from './QueueScreen';
import QRScanner from '../../components/QRScanner';
import OnSession from './OnSession';
import {ActivityIndicator, SafeAreaView, StyleSheet} from 'react-native';
const QRScannerScreen = ({navigation}) => {
  const [isScanAllowed, setScanAllowed] = useState();
  const [isSessionActive, setIsSessionActive] = useState();
  const [isLoading, setIsLoading] = useState(true);
  const getScanAllowed = async () => {
    console.log('Get is QR Available');
    return await fetch(
      Networking.BASE_URL + Networking.SCAN_ALLOWED + global.USER_TOKEN,
      {
        method: 'GET',
        headers: REQUEST_HEADER,
      },
    )
      .then(response => response.json())
      .then(data => {
        console.log('SCAN_ALLOWED: ' + data.detail);
        setScanAllowed(data.detail);
      })
      .catch(error => {
        console.log('ERROR WHILE UPDATING DASHBOARD ' + error.message);
      });
  };
  const getIsSectionActive = async () => {
    const userToken = global.USER_TOKEN;
    return await fetch(
      Networking.BASE_URL + Networking.OCCUPATION + userToken,
      {
        method: 'GET',
        headers: REQUEST_HEADER,
      },
    )
      .then(response => response.json())
      .then(data => {
        console.log('IS_SECTION_ACTIVE: ' + data.detail);
        setIsSessionActive(!data.detail);
      })
      .catch(error => {
        console.log(
          '---QUEUE SCREEN--- ERROR WHILE UPDATING GETTING IS SECTION ACTIVE ' +
            error.message,
        );
      });
  };

  useEffect(() => {
/*    getScanAllowed();
    getIsSectionActive();*/
    const interval = setInterval(async () => {
      await getScanAllowed();
      await getIsSectionActive();
    }, REFRESH_PERIOD);
    setIsLoading(false)
    return () => {
      clearInterval(interval);
    };
  }, []);
  const renderMidScreen = () => {
    if (
      isLoading ||
      isScanAllowed === undefined ||
      isSessionActive === undefined
    ) {
      return (
        <SafeAreaView style={styles.mainContainer}>
          <ActivityIndicator
            animating={true}
            size="large"
            style={styles.spinner}
          />
        </SafeAreaView>
      );
    } else {
      if (isSessionActive) {
        return <OnSession />;
      } else if (isScanAllowed) {
        return <QRScanner navigation={navigation} />;
      } else {
        return <QueueScreen navigation={navigation} />;
      }
    }
  };
  return renderMidScreen();
};

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
  },
  spinner: {alignSelf: 'center'},
});

export default QRScannerScreen;
