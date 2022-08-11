import React, {useEffect, useRef, useState} from 'react';
import {ActivityIndicator, Image, SafeAreaView, StyleSheet} from 'react-native';
import {
  Networking,
  REFRESH_PERIOD,
  REQUEST_HEADER,
} from '../../utils/constants';
import InQueue from './InQueue';
import NotInQueue from './NotInQueue';

const QueueScreen = ({navigation}) => {
  console.log('-----QUEUEE SCREEN RENDERED------');
  const componentMounted = useRef(true);
  const [isLoading, setIsLoading] = useState(true);
  const [isInQueue, setIsInQueue] = useState(true);
  const [peopleCountInQueue, setPeopleCountInQueue] = useState();
  const [queueIndex, setQueueIndex] = useState();
  const userToken = global.USER_TOKEN;

  const leaveQueueCallback = async () => {
    setIsLoading(true);
    await dequeue();
    setIsInQueue(false);
    await getPeopleInQueue();
    setIsLoading(false);
  };
  const queueUpCallback = async () => {
    setIsLoading(true);
    await enqueue();
    setIsInQueue(true);
    await updateQueueIndex();
    setIsLoading(false);
  };

  useEffect(() => {
    let interval;
    if (componentMounted.current) {
      interval = setInterval(() => {
        console.log('Is in queue !!', isInQueue);
        console.log(global.USER_TOKEN);
        getIsInQueue().then(async bool => {
          console.log('Is in Queue??', bool);
          setIsInQueue(bool);
          if (bool) {
            console.log('Updating Queue Index');
            await updateQueueIndex();
          } else {
            console.log('Updating People Count in the Queue');
            await getPeopleInQueue();
          }
          setIsLoading(false);
        });
      }, REFRESH_PERIOD);
    }
    return () => {
      componentMounted.current = false;
      clearInterval(interval);
    };
  }, []);

  //TODO: queue number handling
  const updateQueueIndex = async () => {
    return await fetch(
      Networking.BASE_URL + Networking.QUEUE_INDEX + userToken,
      {
        method: 'GET',
        headers: REQUEST_HEADER,
      },
    )
      .then(response => response.json())
      .then(data => {
        console.log('Queue Num: ', data.detail);
        setQueueIndex(data.detail);
      })
      .catch(error => {
        console.log('ERROR WHILE UPDATING ISINQUEUE ' + error.message);
      });
  };
  const getPeopleInQueue = async () => {
    return await fetch(Networking.BASE_URL + Networking.QUEUE_SIZE, {
      method: 'GET',
      headers: REQUEST_HEADER,
    })
      .then(response => response.json())
      .then(data => {
        console.log('People count in queue: ', data.detail);
        setPeopleCountInQueue(data.detail);
      })
      .catch(error => {
        console.log('ERROR WHILE UPDATING PEOPLEINQUEUE ' + error.message);
      });
  };

  const getIsInQueue = async () => {
    return await fetch(
      Networking.BASE_URL + Networking.QUEUE_INDEX + userToken,
      {
        method: 'GET',
        headers: REQUEST_HEADER,
      },
    )
      .then(response => response.json())
      .then(data => data.detail >= 0)
      .catch(error => {
        console.log('ERROR WHILE UPDATING ISINQUEUE ' + error.message);
      });
  };

  const dequeue = async () => {
    return await fetch(Networking.BASE_URL + Networking.DEQUEUE, {
      method: 'DELETE',
      headers: REQUEST_HEADER,
      body: JSON.stringify({
        user: userToken,
      }),
    }).catch(error => {
      console.log('ERROR WHILE UPDATING DEQUEUE ' + error.message);
    });
  };
  const enqueue = async () => {
    return await fetch(Networking.BASE_URL + Networking.ENQUEUE, {
      method: 'PUT',
      headers: REQUEST_HEADER,
      body: JSON.stringify({
        user: userToken,
      }),
    }).catch(error => {
      console.log('ERROR WHILE UPDATING ENQUEUE ' + error.message);
    });
  };
  const QueueStatusView = () => {
    if (isLoading) {
      return (
        <ActivityIndicator
          animating={true}
          size="large"
          style={styles.spinner}
        />
      );
    } else if (isInQueue) {
      return (
        <InQueue
          navigation={navigation}
          queueIndex={queueIndex}
          parentCallback={leaveQueueCallback}
        />
      );
    } else {
      // Not in queue
      return (
        <NotInQueue
          navigation={navigation}
          peopleInQueue={peopleCountInQueue}
          parentCallback={queueUpCallback}
        />
      );
    }
  };

  return (
    <SafeAreaView style={styles.mainContainer}>
      <Image
        source={require('../../../assets/queue_illust.png')}
        style={styles.image}
      />
      <QueueStatusView />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    justifyContent: 'space-between',
    alignItems: 'center',
    height: '100%',
    width: '95%',
    alignSelf: 'center',
    marginVertical: '3%',
    backgroundColor: '#ddefef',
    borderRadius: 8,
  },
  image: {
    height: '30%',
    width: '100%',
    borderRadius: 10,
  },
  buttonStyle: {
    backgroundColor: '#DD241F',
    borderRadius: 6,
    width: '80%',
    alignItems: 'center',
    justifyContent: 'center',
    height: '10%',
    marginBottom: 70,
  },
  textView: {
    height: '30%',
    width: '100%',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    marginBottom: 35,
  },
  spinner: {alignSelf: 'center'},
  boringText: {fontSize: 35, color: '#000000'},
  messageText: {fontSize: 15, color: '#000000'},
});

export default QueueScreen;
