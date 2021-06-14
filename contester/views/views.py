from contester.models import *
from django.shortcuts import render
from contester.forms import *


def index(request):
    contests = Contest.objects.all()
    tasks = Task.objects.all()
    return render(request, "HomePage.html", {'contests': contests, 'tasks': tasks, 'section': 'contests'})


def profile(request):
    return render(request, "profile_page.html")


def takeFirst(elem):
    return elem[0]


def rating(request):
    users = Account.objects.all()
    user_array = []
    for user in users:
        user_array.append((user.points, user))
    for i in range(len(user_array)):
        for j in range(i + 1, len(user_array)):
            if user_array[i][0] < user_array[j][0]:
                user_array[i], user_array[j] = user_array[j], user_array[i]
    myArray = []
    for i in user_array:
        myArray.append(i[1])

    return render(request, "rating.html", {'user_array': myArray})
