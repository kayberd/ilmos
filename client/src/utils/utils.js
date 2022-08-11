import {AsyncStorage} from 'react-native';
import uuid from 'react-native-uuid';
import { Networking, Notifications, REQUEST_HEADER } from "./constants";
import OneSignal from "react-native-onesignal";
import { useNavigation } from "@react-navigation/native";

export const getUserToken = async () => {
  let token = await AsyncStorage.getItem('token');
  if (token === null) {
    const uuid_ = uuid.v4().toString();
    try {
      await createUser(uuid_)
        .then(response => response.json())
        .then(async response => {
          if (response.detail === 'Success') {
            await AsyncStorage.setItem('token', uuid_);
            console.log('Token is set now!!');
            console.log(uuid_);
            token = uuid_;
          } else if (response.detail === 'Exists') {
            console.log('User does exist');
            token = uuid_;
          }
        })
        .catch(e => {
          console.log('ERROR WHILE CREATING A NEW USER' + e);
        });
    } catch (e) {
      console.log('ERROR WHILE SETTING USER_TOKEN INTO ASYNC: ' + e);
    }
  }
  return token;
};

export const occupySeat = async seatId => {
  let user_token = await getUserToken();
  console.log(user_token);
  return await fetch(Networking.BASE_URL + Networking.OCCUPY + seatId, {
    method: 'PUT',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user: user_token,
      // deviceToken:deviceToken,
    }),
  })
    .then(response => response.json())
    .catch(error => {
      console.log(
        'There has been a problem with your fetch operation: ' + error.message,
      );
      throw error;
    });
};

export const createUser = async token => {
  return await fetch(Networking.BASE_URL + Networking.NEW_USER, {
    method: 'POST',
    headers: REQUEST_HEADER,
    body: JSON.stringify({
      user: token,
    }),
  }).catch(error => {
    console.log('ERROR WHILE UPDATING DASHBOARD ' + error.message);
  });
};

export const oneSignalSetup = () => {
  OneSignal.setExternalUserId(global.USER_TOKEN, (results) => {
    // The results will contain push and email success statuses
    console.log('Results of setting external user id');
    console.log(results);
    console.log(global.USER_TOKEN);
    // Push can be expected in almost every situation with a success status, but
    // as a pre-caution its good to verify it exists
    if (results.push && results.push.success) {
      console.log('Results of setting external user id push status:');
      console.log(results.push.success);
    }
  });
  OneSignal.setLogLevel(6, 0);
  OneSignal.setAppId(Notifications.APP_ID);
};


