import React, {useEffect, useRef, useState} from 'react';
import {
  FlatList,
  StyleSheet,
  View,
  ActivityIndicator,
  Button,
  Platform,
  Linking,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import OneSignal from 'react-native-onesignal';
// import uuid from 'react-native-uuid';

import {
  Networking,
  MAX_SEAT_NUM,
  TABLE_CAPACITY,
  REFRESH_PERIOD,
  Notifications,
} from '../../utils/constants';
import User from '../../components/User';

// import {messaging} from '@react-native-firebase/messaging';

const Dashboard = () => {
  const oneSignalSetup = () => {
    OneSignal.setExternalUserId(global.USER_TOKEN, results => {
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
    //Prompt for push on iOS
    OneSignal.promptForPushNotificationsWithUserResponse(response => {
      console.log('Prompt response #334: ', response);
    });
    //Method for handling notifications recieved while app in foreground
    OneSignal.setNotificationWillShowInForegroundHandler(
      notificationReceivedEvent => {
        console.log(
          'One Signal: notiication will show in foreground: ',
          notificationReceivedEvent,
        );
        let notification = notificationReceivedEvent.getNotification();
        console.log('notification: ', notification);
        const data = notification.additionalData;
        console.log('additionalData: ', data);
        //Complete with null means don't show a notification
        notificationReceivedEvent.complete(notification);
      },
    );
    //Method for handling notifications opened
    OneSignal.setNotificationOpenedHandler(notification => {
      console.log('OneSignal: notification opened: ', notification);
    });
    // REMOTE NOTIFICATIONS SETUP END //
  };
  function handleOpenURL(evt) {
    console.warn(evt.url);
    // do something with the url
  }

  Linking.addEventListener('url', handleOpenURL);

  const initSeats = [
    {
      table_id: 1,
      seats: [
        {seatId: 1, status: 'TAKEN'},
        {seatId: 2, status: 'TAKEN'},
        {seatId: 3, status: 'TAKEN'},
        {seatId: 4, status: 'TAKEN'},
      ],
    },
    {
      table_id: 2,
      seats: [
        {seatId: 1, status: 'TAKEN'},
        {seatId: 2, status: 'TAKEN'},
        {seatId: 3, status: 'TAKEN'},
        {seatId: 4, status: 'TAKEN'},
      ],
    },
    {
      table_id: 3,
      seats: [
        {seatId: 1, status: 'TAKEN'},
        {seatId: 2, status: 'TAKEN'},
        {seatId: 3, status: 'TAKEN'},
        {seatId: 4, status: 'TAKEN'},
      ],
    },
    {
      table_id: 4,
      seats: [
        {seatId: 1, status: 'TAKEN'},
        {seatId: 2, status: 'TAKEN'},
        {seatId: 3, status: 'TAKEN'},
        {seatId: 4, status: 'TAKEN'},
      ],
    },
  ];
  const [tables, setTables] = useState(initSeats);
  const [loading, setLoading] = useState(true);
  const componentMounted = useRef(true);
  useEffect(() => {
    let interval;
    if (componentMounted.current) {
      interval = setInterval(() => {
        updateDashboard();
      }, REFRESH_PERIOD);
    }
    return () => {
      componentMounted.current = false;
      clearInterval(interval);
    };
  }, []);

  const updateDashboard = () => {
    console.log('UPDATING THE VIEW');
    const parseSeats = seats_arg => {
      let parsedSeats = [];
      for (let i = 0; i < MAX_SEAT_NUM; i += TABLE_CAPACITY) {
        let table = {
          table_id: i,
          seats: [
            seats_arg[i],
            seats_arg[i + 1],
            seats_arg[i + 2],
            seats_arg[i + 3],
          ],
        };
        parsedSeats.push(table);
      }

      return parsedSeats;
    };
    const getDashboardData = async () => {
      return await fetch(Networking.BASE_URL + Networking.SEATS, {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      })
        .then(response => response.json())
        .catch(error => {
          console.log('ERROR WHILE UPDATING DASHBOARD ' + error.message);
        });
    };

    getDashboardData()
      .then(json => {
        let parsedSeats = parseSeats(json);
        setTables(parsedSeats);
        setLoading(false);
      })
      .catch(error =>
        console.log('ERROR WHILE UPDATING DASHBOARD ' + error.message),
      );
  };

  const getDashboardData = async () => {
    return await fetch(Networking.BASE_URL + Networking.SEATS, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .catch(error => {
        console.log('ERROR WHILE UPDATING DASHBOARD ' + error.message);
      });
  };

  const renderItem = item => {
    if (item) {
      return (
        <View style={styles.table}>
          <User seatStatus={item.item.seats[2].status} />
          <User seatStatus={item.item.seats[3].status} />
          <User seatStatus={item.item.seats[0].status} />
          <User seatStatus={item.item.seats[1].status} />
        </View>
      );
    } else {
      return null;
    }
  };

  // updateDashboard();

  return (
    <SafeAreaView style={styles.content}>
      <View style={styles.plate}>
        {/*<View style={styles.room_title_view}>
          <Text style={styles.room_title}>METU CENG Study Hall</Text>
        </View>*/}
        {/*<Button title="Print uuid" onPress={() => oneSignalSetup()} />*/}
        {loading ? (
          <ActivityIndicator animating={loading} size="large" />
        ) : (
          <FlatList
            numColumns={2}
            inverted
            data={tables}
            renderItem={renderItem}
            contentContainerStyle={styles.flatlistContainer}
          />
        )}
      </View>
    </SafeAreaView>
  );
};

//DON'T EVEN THINK TO TOUCH BELOW CSS

const styles = StyleSheet.create({
  content: {
    flex: 1,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  plate: {
    backgroundColor: '#e0e6e7',
    width: '90%',
    height: '80%',
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  flatlistContainer: {
    flex: 1,
    justifyContent: 'space-evenly',
  },
  table: {
    marginHorizontal: 12,
    flexDirection: 'row',
    flexWrap: 'wrap',
    backgroundColor: '#ffffff',
    margin: 1,
    width: '42%',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    padding: '2%',
  },
  /*room_title: {
    fontFamily: 'Sans-Serif',
    fontSize: 15,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#ff0000',
  },
  room_title_view: {
    padding: '2%',
    marginTop: '10%',
  },*/
});

export default Dashboard;
