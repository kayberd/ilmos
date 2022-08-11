import * as React from 'react';

import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';

import QRScannerScreen from './QRScreen/QRScannerScreen';
import Dashboard from './Dashboard/Dashboard';
import ProfileScreen from './ProfileScreen/ProfileScreen';

import {cameraAndQRIcon, homeIcon, profileIcon} from '../utils/icons';

const Tab = createBottomTabNavigator();

const BottomTabs = () => {
  return (
    <Tab.Navigator
      initialRouteName="Dashboard"
      screenOptions={{
        tabBarActiveTintColor: '#e91e63',
        tabBarActiveBackgroundColor: '#f3f3f3',
      }}>
      <Tab.Screen
        name="Dashboard"
        component={Dashboard}
        options={{
          headerTitle: 'DASHBOARD',
          tabBarLabel: 'Dashboard',
          tabBarItemStyle: {marginBottom: 4},
          headerTitleAlign: 'center',
          headerTitleStyle: {fontSize: 17},
          tabBarIcon: () => homeIcon,
          unmountOnBlur: true,
        }}
      />
      <Tab.Screen
        name="Scan QR"
        component={QRScannerScreen}
        initialParams={{test: 'Test Param'}}
        options={{
          headerTitle: 'SCAN QR',
          headerTitleStyle: {fontSize: 17},
          tabBarLabel: 'Scan QR',
          tabBarItemStyle: {marginBottom: 4},
          headerTitleAlign: 'center',
          tabBarIcon: cameraAndQRIcon,
          unmountOnBlur: true,
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          headerTitle: 'PROFILE',
          headerTitleStyle: {fontSize: 17},
          tabBarLabel: 'Profile',
          tabBarItemStyle: {marginBottom: 4},
          headerTitleAlign: 'center',
          tabBarIcon: () => profileIcon,
          unmountOnBlur: true,
        }}
      />
      {/*<Tab.Screen name="FCMTest" component={FcmTest} />*/}
      {/*<Tab.Screen
        name="Queue"
        component={QueueScreen}
        options={{
          tabBarLabel: 'QUEUE',
          headerTitleAlign: 'center',
          unmountOnBlur: false,
        }}
      />*/}
    </Tab.Navigator>
  );
};

export default BottomTabs;
