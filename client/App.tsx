/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * Generated with the TypeScript template
 * https://github.com/react-native-community/react-native-template-typescript
 *
 * @format
 */

import {NavigationContainer} from '@react-navigation/native';
import React from 'react';
import BottomTabs from './src/screens/BottomTabs';
import RNBootSplash from 'react-native-bootsplash';
import {LogBox} from 'react-native';

const App = () => {
  LogBox.ignoreAllLogs();

  return (
    <NavigationContainer onReady={() => RNBootSplash.hide()}>
      <BottomTabs />
    </NavigationContainer>
  );
};

export default App;
