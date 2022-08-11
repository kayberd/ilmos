/**
 * @format
 */

import {AppRegistry} from 'react-native';
import App from './App';
import {name as appName} from './app.json';
import 'react-native-gesture-handler';
import './src/utils/utils';
import {getUserToken, oneSignalSetup} from './src/utils/utils';

getUserToken().then(token => {
  global.USER_TOKEN = token;
  oneSignalSetup();
});

AppRegistry.registerComponent(appName, () => App);
