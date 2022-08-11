import * as React from 'react';

import {Text} from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

export const homeIcon = <Icon name="home" size={28} color="#183153" />;
export const profileIcon = <Icon name="user" size={28} color="#183153" />;
export const customQr = <Icon name="qrcode" size={20} color="#183153" />;
export const cameraIcon = <Icon name="camera" size={20} color="#183153" />;

export const GearsIcon = () => <Icon name="gears" size={50} color="#000000" />;
export const CoffeeIcon = () => (
  <Icon name="coffee" size={50} color="#000000" />
);

export const cameraAndQRIcon = () => (
  <Text>
    {cameraIcon} {customQr}
  </Text>
);
