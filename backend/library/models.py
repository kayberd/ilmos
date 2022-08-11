from django.db import models
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import status



class Seat(models.Model):
    seatId = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=16, default='VACANT')


    def __str__(self):
        return f"seatId: {self.seatId}, status: {self.status}"


    def is_full():
        seats = Seat.objects.all()

        for seat in seats:
            if seat.status == 'VACANT':
                return False
        
        return True

    def avail_seat_count():
        return len(Seat.objects.filter(status='VACANT'))


class User(models.Model):
    # userId = models.IntegerField(primary_key=True)
    token = models.TextField(primary_key=True)

    def __str__(self):
        return f"token: {self.token}"


class Occupation(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startTime = models.DateTimeField(default=timezone.now)
    breakTime = models.DateTimeField(null=True)

    def __str__(self):
        return f"seat: {self.seat}, user: {self.user}, startTime: {self.startTime}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['seat', 'user'], name='unique_occupation'),
            models.UniqueConstraint(fields=['seat'], name='unique_seat'),
            models.UniqueConstraint(fields=['user'], name='unique_user'),
        ]

        order_with_respect_to = 'startTime'


class Queue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startTime = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user'], name='unique_user_in_queue')
    #     ]

    def __str__(self):
        return f"user: {self.user}, startTime: {self.startTime}"


    """
        returns true if the queue is empty
    """
    def empty():
        return not Queue.objects.all().exists()


    def size():
        return len(Queue.objects.all())


    def get_index(token):
        queue = Queue.objects.all()

        for idx, elem in enumerate(queue):
            if elem.user.token == token:
                return Response({'detail': idx}, status=status.HTTP_200_OK)

        return Response({'detail': -1}, status=status.HTTP_200_OK) 


class Admin(models.Model):
    user = models.CharField(primary_key=True, max_length=15)
    password = models.CharField(max_length=32) 


    def __str__(self):
        return f'user: {self.user}, password: {self.password}'
