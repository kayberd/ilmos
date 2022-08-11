from django.urls import path
from library import views

urlpatterns = [
    path('seats/', views.seats),
    path('seat/<int:pk>', views.SeatDetail.as_view()),

    path('users/', views.UserList.as_view()),
    path('user/<str:pk>', views.UserDetail.as_view()),
    path('new-user/', views.createUser),

    path('occupations/', views.list_occupations),
    path('occupation/<str:pk>', views.OccupationDetail.as_view()),
    path('is-full/', views.is_full),
    path('scan-allowed/<str:token>', views.scan_allowed),
    
    path('queue/', views.QueueList.as_view()),
    path('queue-elem/<int:pk>', views.QueueDetail.as_view()),
    path('enqueue/', views.enqueue),
    path('dequeue/', views.dequeue_handler),
    path('queue-index/<str:token>', views.queue_index),
    path('queue-size/', views.queue_size),
    path('dequeue/<str:token>', views.dequeue_spec_user),
    path('in-queue/', views.in_queue),

    path('occupy/<int:pk>', views.OccupyDetail.as_view()),
    path('release/<int:pk>', views.ReleaseDetail.as_view()),

    path('sendSMS/', views.sendSMS),

    path('auth/', views.auth),
]