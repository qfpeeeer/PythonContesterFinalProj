from django.shortcuts import render
import time
from datetime import timedelta, datetime

from contester.forms import DocumentForm
from contester.models import *


def sort(request):
    tasks = Task.objects.all()

    section = request.GET.get('section')

    val1 = request.GET.get('val1')
    val2 = request.GET.get('val2')
    val3 = request.GET.get('val3').split(",")

    items = Contest.objects.all()
    res = []

    if val1 == "undefined" and val2 == "undefined" and len(val3) == 1:
        return render(request, "index/HomePage.html", {'contests': res, 'tasks': tasks, 'section': 'contests'})

    if section.lower() == 'tasks':
        items = tasks

    for item in items:
        check = any(it in item.topics for it in val3)
        check2 = item.complexity == val2

        if (check or val3[0] == "") and (val2 == "undefined" or check2):
            res.append(item)

    if val1 == "popular":
        result = sorted(items, key=lambda it: it.user_counter)

    if section.lower() == 'tasks':
        return render(request, "index/HomePage.html", {'contests': items, 'tasks': res, 'section': 'tasks'})

    return render(request, "index/HomePage.html", {'contests': res, 'tasks': items, 'section': 'contests'})


def contest(request, id):
    contest = Contest.objects.get(pk=id)
    print(contest.tasks.all())
    sum = 0
    for task in contest.tasks.all():
        sum = sum + task.points

    return render(request, "Contest_page.html", {'contest': contest, 'points': sum})


def convert_from_ms(seconds):
    minutes = seconds / 60
    minutes = round(int(minutes), 0)
    hours = round(int(minutes)/60, 0)
    return int(hours), int(minutes), int(seconds%60)


def getTaskByIdForContest(request, contest_id, task_id):
    contest = Contest.objects.get(pk=contest_id)
    task = Task.objects.get(pk=task_id)

    left = ((contest.start_time + timedelta(minutes=contest.duration)).timestamp() - time.time())
    finished = None
    if left < 0:
        finished = True

    form = DocumentForm()
    my_submits_qs = ContestSubmit.objects.filter(contest_id=contest_id, user_id=request.user.id, task_id=task_id)
    my_submits = []
    has_accepted = False
    for submit in my_submits_qs:
        status = "Fail"
        if submit.is_accepted:
            status = "Accepted"
            has_accepted = True
        my_submits.append(
            {"status": status, "points": round(submit.points),
             "date": submit.submited_at.strftime("%m/%d/%Y, %H:%M:%S")})
    hours, minutes, seconds = convert_from_ms(left)
    return render(request, "contest_task_page.html", {'contest': contest, 'task': task, 'finished': finished, 'form': form, 'my_submits': my_submits,
                                                      'left': "Time left: " + str(hours) +':'+ str(minutes) + ":" + str(seconds)})
