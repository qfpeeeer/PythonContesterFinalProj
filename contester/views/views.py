from django.http import HttpResponse

from contester.models import *
from django.shortcuts import render
from contester.forms import *


def index(request):
    contests = Contest.objects.all()
    tasks = Task.objects.all()
    notify = Notification.objects.filter(user_id=request.user.id)
    return render(request, "index/HomePage.html", {'contests': contests, 'tasks': tasks, 'section': 'contests',
                                                   'notifications':notify})


def profile(request):
    return render(request, "profile_page.html")


def takeFirst(elem):
    return elem[0]


def rating(request):
    users = Account.objects.all()
    users = list(users)
    return render(request, "rating.html", {'users': users})

# def rating(request):
#     users = Account.objects.all()
#     user_array = []
#     for user in users:
#         user_array.append((user.points, user))
#     for i in range(len(user_array)):
#         for j in range(i + 1, len(user_array)):
#             if user_array[i][0] < user_array[j][0]:
#                 user_array[i], user_array[j] = user_array[j], user_array[i]
#     myArray = []
#     for i in user_array:
#         myArray.append(i[1])
#
#     return render(request, "rating.html", {'users': myArray})


def notify(request):
    user = request.user
    notification = Notification.objects.filter(user_id=user.id)
    if notification is not None:
        return HttpResponse(notification[0].description)


def deleteNotification(request):
    user = request.user
    notification = Notification.objects.filter(user_id=user.id)
    notification.delete()

    return HttpResponse("deleted")


def update(request):
    if request.method == "POST":

        user = request.user
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        # print(email)

        current = Account.objects.get(email= email)
        # print(current.lastname)
        current.email = email
        current.firstname = firstname
        current.lastname = lastname
        current.username = username
        # print(current)
        current.save()

    return render(request, "profile_page.html")
