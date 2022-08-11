from rest_framework import serializers
from library.models import *

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['seatId', 'status']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['token']

class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = ['seat', 'user', 'startTime', 'breakTime']

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ['user', 'startTime']