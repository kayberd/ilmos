import React from 'react';
import {Button, Text, View} from 'react-native';
import Modal from 'react-native-modal';

function RoomFullModal({
  navigation,
  isModalVisible,
  setIsModalVisible,
  isAllOccupied,
}) {
  const toggleModal = () => {
    setIsModalVisible(!isModalVisible);
  };

  return (
    <Modal isVisible={isModalVisible && !isAllOccupied}>
      <View style={{flex: 0.3, backgroundColor: '#e0e6e7', borderRadius: 8}}>
        <Text>Hello!</Text>
        <Button
          title="Hide modal"
          onPress={toggleModal}
          style={{width: '80%'}}
        />
      </View>
    </Modal>
  );
}

export default RoomFullModal;
