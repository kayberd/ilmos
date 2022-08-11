from library.models import *
from library.serializers import *
from library.utils import sanitize, break_timeout, qr_timeout, release_seat

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid
import threading
from time import time
import os
import requests

from library.repeat_timer import RepeatTimer
from library.utils import notify, dequeue

from twilio.rest import Client


breakL = list()
qrL = list()

mutex_break = threading.Lock()
mutex_qr = threading.Lock()

break_timer = RepeatTimer(5, break_timeout, args=(breakL, qrL, mutex_break, mutex_qr))
qr_timer = RepeatTimer(5, qr_timeout, args=(qrL, mutex_qr))
break_timer.start()
qr_timer.start()



@api_view(['POST'])
def createUser(request):

    if not request.data.__contains__('user'):
        return Response({'detail': 'Request body should have "user" as a key.'}, status=status.HTTP_400_BAD_REQUEST)

    token = request.data['user']

    if User.objects.filter(token=token).exists():
        return Response({'detail': 'Exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User(token=token)
    user.save()
    return Response({'detail': 'Success'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def sendSMS(request):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='parsecs?',
            from_='+12058394906',
            to='+905530633975'
        )

    return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'OPTIONS'])
def auth(request):
    if request.method == "OPTIONS":
        print('AUTH OPTIONS RECEIVED')
        return Response(headers={'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Method': '*'}, status=status.HTTP_204_NO_CONTENT)

    print('POST RECEIVED')
    print(type(request.method))
    print(request.data)

    uname = request.data.get('username')
    pwd = request.data.get('password')

    try:
        priviledged_user = Admin.objects.get(user=uname)
    except Admin.DoesNotExist:
        return Response({'detail': 'Incorrect username or password.'}, status=status.HTTP_400_BAD_REQUEST)

    if pwd != priviledged_user.password:
        return Response({'detail': 'Incorrect username or password.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(headers={'Access-Control-Allow-Origin': '*',
                             'Access-Control-Allow-Headers': '*',
                             'Access-Control-Allow-Method': '*'}, status=status.HTTP_200_OK)


# User-related views.
class UserList(APIView):
    """
    List all Users, or create a new User.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a User instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'OPTIONS'])
def seats(request):

    if request.method == "OPTIONS":
        print(f'SEATS: OPTIONS')
        return Response(headers={'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Method': '*'}, status=status.HTTP_204_NO_CONTENT)

    query = 'SELECT * FROM library_seat ORDER BY "seatId" ASC;'
    seats = Seat.objects.raw(query)
    serializer = SeatSerializer(seats, many=True)
    return Response(serializer.data)


class SeatDetail(APIView):
    """
    Retrieve, update or delete a Seat instance.
    """
    def get_object(self, pk):
        try:
            return Seat.objects.get(pk=pk)
        except Seat.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        seat = self.get_object(pk)
        serializer = SeatSerializer(seat)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        seat = self.get_object(pk)

        if request.data.__contains__('status') and request.data['status'] in ['VACANT', 'TAKEN']:

            mutex_break.acquire()

            if seat.status == 'BREAK' and request.data['status'] == 'TAKEN':        # breakten takene gecerken
                seat.status = 'TAKEN'
                seat.save()

                occupation = get_object_or_404(Occupation, seat=seat)
                occupation.startTime = timezone.now()
                occupation.breakTime = None
                occupation.save()

                for d in breakL:
                    if d['id'] == seat.seatId:
                        breakL.remove(d)

            elif seat.status == 'TAKEN' and request.data['status'] == 'VACANT':         # takendan breake gecerken
                seat.status = 'BREAK'
                seat.save()

                occupation = get_object_or_404(Occupation, seat=seat)
                occupation.breakTime = timezone.now()
                occupation.save()

                breakL.append({'id': seat.seatId, 'time': time(), 'notified': False})

            mutex_break.release()

            return Response(status=status.HTTP_200_OK)

        return Response({'detail': "Request body should contain status field and status field can be 'VACANT' or 'TAKEN'."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_occupations(request):
    occupations = Occupation.objects.all()
    serializer = OccupationSerializer(occupations, many=True)
    return Response(serializer.data)


class OccupationDetail(APIView):
    
    def get_object(self, pk):
        user = None
        try:
            user = User.objects.get(token=pk)
        except User.DoesNotExist:
            raise Http404('User does not exist.')

        occupation = None
        try:
            occupation = Occupation.objects.get(user=user)
        except Occupation.DoesNotExist:
            raise Http404
        
        return occupation

    def get(self, request, pk, format=None):
        try:
            occupation = self.get_object(pk)
        except Http404:
            return Response({'detail': 'User not found or user is not involved in an occupation.'})    

        serializer = OccupationSerializer(occupation)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def scan_allowed(request, token):

    user = get_object_or_404(User, token=token)
    
    if Occupation.objects.filter(user=user).exists():
        return Response({'detail': False}, status=status.HTTP_200_OK)
    elif Seat.is_full():
        return Response({'detail': False}, status=status.HTTP_200_OK)
    elif Queue.empty():
        return Response({'detail': True}, status=status.HTTP_200_OK)
    elif Queue.get_index(token).data['detail'] == -1:
        return Response({'detail': False}, status=status.HTTP_200_OK)
    else:
        location = Queue.get_index(token)
        avail_count = Seat.avail_seat_count()
        
        if location.data['detail'] < avail_count:
            return Response({'detail': True}, status=status.HTTP_200_OK)
        
        return Response({'detail': False}, status=status.HTTP_200_OK)


@api_view(['GET'])
def is_full(request):
    full = Seat.is_full()

    if full:
        return Response({'detail': True}, status=status.HTTP_200_OK)   
    return Response({'detail': False}, status=status.HTTP_200_OK)   


class QueueList(APIView):

    def get(self, request, format=None):
        query = 'SELECT * FROM library_queue ORDER BY "startTime" ASC;'
        queue = Queue.objects.raw(query)
        serializer = QueueSerializer(queue, many=True)
        return Response(serializer.data)

    def put(self, request, format=None):
        serializer = QueueSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        req = request.data
        uid = req['user']
        
        try:
            queue_object = Queue.objects.get(user=uid)
            queue_object.delete()
        except Queue.DoesNotExist:
            return Response({"detail": f'There is no user {uid} in the queue!'}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT) 


class QueueDetail(APIView):
    pass


@api_view(['PUT'])
def enqueue(request):

    # if not Seat.is_full():
    #     return Response({'detail': 'There are vacant desks, cannot queue up.'}, status=status.HTTP_400_BAD_REQUEST)

    if not request.data.__contains__('user'):
        return Response({'detail': 'Request body should have "user" as a key!'}, status=status.HTTP_400_BAD_REQUEST)

    token = request.data['user']
    user = get_object_or_404(User, token=token)

    user = None
    try:
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if Queue.objects.filter(user=user).exists():
        return Response({'detail': 'User is already in the queue!'}, status=status.HTTP_400_BAD_REQUEST)

    queue_instance = Queue(user=user)     
    queue_instance.save()

    return Response({'user': f'{user.token}', 'startTime': f'{queue_instance.startTime}', 'index': Queue.size()-1}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def dequeue_handler(request):

    if not request.data.__contains__('user'):
        return dequeue()

    else:
        user = None
        try:
            user = User.objects.get(token=request.data['user'])
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)

        queue_instance = None
        try:
            queue_instance = Queue.objects.get(user=user)
        except Queue.DoesNotExist:
            return Response({'detail': 'User is not in the queue!'}, status=status.HTTP_400_BAD_REQUEST)

        queue_instance.delete()
        return Response({'detail': 'Succes.'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def dequeue_spec_user(request, token):
    user = None
    try:
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return Response({'detail': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)

    queue_instance = None
    try:
        queue_instance = Queue.objects.get(user=user)
    except Queue.DoesNotExist:
        return Response({'detail': 'User is not in the queue!'}, status=status.HTTP_400_BAD_REQUEST)

    queue_instance.delete()
    return Response({'detail': 'Succes.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def queue_index(request, token):
    return Queue.get_index(token)


@api_view(['GET'])
def queue_size(request):
    return Response({'detail': Queue.size()}, status=status.HTTP_200_OK)


@api_view(['GET'])
def in_queue(request):
    if not request.data.__contains__('user'):
        return Response({'detail': 'Request body should have "user" as a key.'}, status=status.HTTP_400_BAD_REQUEST)

    user = None
    try:
        user = User.objects.get(token=request.data['user'])
    except User.DoesNotExist:
        return Response({'detail': False}, status=status.HTTP_200_OK)

    queue_instance = None
    try:
        queue_instance = Queue.objects.get(user=user)
    except Queue.DoesNotExist:
        return Response({'detail': False})

    return Response({'detail': True}, status=status.HTTP_200_OK)


class OccupyDetail(APIView):

    def get_object(self, pk):
        seat = get_object_or_404(Seat, seatId=pk)
        return get_object_or_404(Occupation, seat=seat)

    def get(self, request, pk, format=None):
        occupation = self.get_object(pk)
        serializer = OccupationSerializer(occupation)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if not request.data.__contains__('user'):
            return Response({'detail': "Request body should have 'user' as a key!"}, status=status.HTTP_400_BAD_REQUEST)

        seat = get_object_or_404(Seat, seatId=pk)

        if Occupation.objects.filter(seat=seat).exists():
            return Response({'detail': 'Seat is not empty!'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, token=request.data['user'])

        if Occupation.objects.filter(user=user).exists():
            return Response({'detail': 'Same user cannot be seated on different seats!'}, status=status.HTTP_400_BAD_REQUEST)

        if not Queue.empty() and user != Queue.objects.all()[0].user:
            return Response({'detail': 'Seat is only available for the person in front of the queue!'}, status=status.HTTP_400_BAD_REQUEST)

        elif not Queue.empty():
            dequeue()

        seat.status = 'TAKEN'
        seat.save()

        occupation = Occupation(seat=seat, user=user)
        occupation.save()

        return Response({'detail': 'Success'}, status=status.HTTP_201_CREATED)


class ReleaseDetail(APIView):

    def delete(self, request, pk, format=None):
        if not request.data.__contains__('user'):
            return Response({'detail': "Request body should have 'user' as a key!"}, status=status.HTTP_400_BAD_REQUEST)

        seat = get_object_or_404(Seat, seatId=pk)

        if not Occupation.objects.filter(seat=seat).exists():
            return Response({'detail': 'Seat is already empty!'}, status=status.HTTP_400_BAD_REQUEST)

        release_seat(seat, mutex_qr, qrL)

        return Response({'detail': f'Seat {seat.seatId} is released.'}, status=status.HTTP_200_OK)

