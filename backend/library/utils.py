from time import sleep, time
import requests
import os

from library.models import *

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from twilio.rest import Client


def release_seat(seat, mutex_qr, qrL):
    seat.status = 'VACANT'
    seat.save()

    occupation = get_object_or_404(Occupation, seat=seat)
    occupation.delete()

    if Queue.objects.all().exists():
        avail_count = Seat.avail_seat_count()
        queue_size = Queue.size()

        if avail_count <= queue_size:
            notified = Queue.objects.all()[avail_count-1]
            token = notified.user.token
            notify(token, 'You can take a seat now.', 'Your turn!')

            mutex_qr.acquire()
            qrL.append({'token': token, 'time': time()})
            mutex_qr.release()


def sendSMS(seat):
    # account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    # auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    # client = Client(account_sid, auth_token)

    # message = client.messages \
    #     .create(
    #         body=f'Please clear desk {seat}.',
    #         from_='+12058394906',
    #         to='+905530633975'
    #     )


    pass # 15 dolardan 11 dolar kalmis


def get_user_of_seat(seat_id):
    seat = None
    try:
        seat = Seat.objects.get(seatId=seat_id)
    except Seat.DoesNotExist:
        return Response({'detail': f'There is no seat with id {seat_id}'}, status=status.HTTP_400_BAD_REQUEST)

    occupation = None
    try:
        occupation = Occupation.objects.get(seat=seat)
    except Occupation.DoesNotExist:
        return Response({'detail': 'User is not sitting in this seat.'}, status=status.HTTP_400_BAD_REQUEST)

    token = occupation.user.token
    return token


def sanitize(qu, seatId, breakL, mutex):
    # print('Thd started.')

    while True:
        status = qu.get()
        noise = False

        for _ in range(3):
            sleep(2)
            if not qu.empty():
                qu.get()        # qu'yu tamamen bosaltma, TVT geldiginde sicar
                noise = True
                break

        if not noise:
            # print('not noise')

            seat = Seat.objects.get(seatId=seatId)

            if seat.status == 'BREAK' and status == 'TAKEN':
                seat.status = 'TAKEN'
                seat.save()

                mutex.acquire()
                
                for d in breakL:
                    if d['id'] == seatId:
                        breakL.remove(d)

                mutex.release()
                # print(f'Seat {seat.seatId} set to TAKEN')

            elif seat.status == 'TAKEN' and status == 'VACANT':
                seat.status = 'BREAK'
                seat.save()

                mutex.acquire()
                breakL.append({'id': seat.seatId, 'time': time()})
                mutex.release()
                # print(f'Seat {seat.seatId} set to BREAK')


def qr_timeout(qrL, mutex):
    print('In qr timeout')

    mutex.acquire()

    for d in qrL:
        print(d)

        token = d['token']

        if time() - d['time'] > 10:
            print('should dequeue')
            user = get_object_or_404(User, token=token)
            queue_instance = get_object_or_404(Queue, user=user)
            queue_instance.delete()

            qrL.remove(d)

    mutex.release()


def break_timeout(breakL, qrL, mutex_break, mutex_qr):
    print('In break_timeout')

    mutex_break.acquire()

    for d in breakL:
        seat_id = d['id']
        token = get_user_of_seat(seat_id)

        if not d['notified'] and time() - d['time'] > 15:
            notify(token, 'You may consider going back to your seat.', 'Your break is about to end')
            d['notified'] = True

        elif time() - d['time'] > 10:
            seat = Seat.objects.get(seatId=d['id'])

            release_seat(seat, mutex_qr, qrL)
            notify(token, 'We had to kick you out.', 'You exceeded your time limit')
            sendSMS(seat_id)

            breakL.remove(d)

    mutex_break.release()


def notify(token, message, heading):

    url = "https://onesignal.com/api/v1/notifications"

    payload = {
        "app_id": '7624b802-16e2-454b-a759-856384f5382d',
        # "included_segments": ["Subscribed Users"],
        "include_external_user_ids": [token],
        "contents": {
            "en": message,
            "es": "Spanish Message",
        },
        "headings": {
            "en": heading
        },
        "name": "INTERNAL_CAMPAIGN_NAME"
    }
    headers = {
        "Accept": "application/json",
        "Authorization": "Basic ZjhiZTMxZDMtYTdmMi00MmNlLTlmOTAtZGI4ZDIxMmVkMTQ3",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)


def dequeue():
    query = 'SELECT * FROM library_queue ORDER BY "startTime" ASC;'
    queue = Queue.objects.raw(query)

    if len(list(queue)) != 0:
        token = queue[0].user.token
        queue[0].delete()
        return Response({'detail': f'User {token} is removed from the queue.'}, status=status.HTTP_200_OK)

    return Response({'detail': 'Queue is empty!'}, status=status.HTTP_400_BAD_REQUEST)

