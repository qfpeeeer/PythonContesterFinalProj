import os
import pathlib
import shutil
import stat
import subprocess

from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages  # import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .checker import checker
from .forms import *


# Create your views here.


def index(request):
    contests = Contest.objects.all()
    tasks = Task.objects.all()
    return render(request, "HomePage.html", {'contests': contests, 'tasks': tasks})


def auth(request):
    return render(request, "Auth.html")


def test(request):
    return render(request, "bootstrap/test_page.html")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(str(password))
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="Auth.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


def profile(request):
    return render(request, "profile_page.html")


def rating(request):
    users = Account.objects.all()
    users = list(users)
    users.sort(key=lambda x: x.rating, reverse=True)
    return render(request, "rating.html", {'users': users})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render(request=request, template_name="Auth.html", context={"register_form": form})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = Account.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Python Contester',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def runscript(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = request.POST.get('task_id', None)
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            print(newdoc.docfile)
            new_path = str(pathlib.Path(newdoc.docfile.path).parent) + '/' + str(newdoc.id) + \
                       str(pathlib.Path(newdoc.docfile.path).suffix)
            print(new_path)
            print(newdoc.docfile.name)

            os.rename(newdoc.docfile.path, new_path)
            newdoc.docfile.name = "codes/" + str(newdoc.id) + str(pathlib.Path(newdoc.docfile.path).suffix)
            newdoc.save()
            result, numberOfTestCases = checker(newdoc.docfile, task_id)
            res = 0
            for i in result:
                res += i
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            task = Task.objects.get(pk=task_id)
            taskLink = "http://127.0.0.1:8000/task/" + str(task_id)
            if res == numberOfTestCases:
                return render(request, 'results.html',
                              {'res': res, 'task_id': task_id, 'task': task, "taskLink": taskLink,
                               'totalNumOfTestCases': numberOfTestCases, "accepted": 1})
            else:
                return render(request, 'results.html',
                              {'res': res, 'task_id': task_id, 'task': task, "taskLink": taskLink,
                               'totalNumOfTestCases': numberOfTestCases, "failed": 1})

    return render(request, 'results.html')


def list(request):
    documents = Document.objects.all()
    return render(request, 'list.html', {'documents': documents})


def suggest_task(request):
    return render(request, 'suggest_task.html')


def getTaskById(request, id):
    task = Task.objects.get(pk=id)
    form = DocumentForm()
    return render(request, 'task_page.html', {'task': task, 'form': form, 'task_id': id})


def suggestingTask(request):
    form = SuggestingTaskForm()


def createTask(request):
    if request.method == 'POST':
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        idescription = request.POST.get('idescription', None)
        odescription = request.POST.get('odescription', None)
        complexity = request.POST.get('complexity', None)
        topics = [request.POST.get('topics', None)]
        points = request.POST.get('points', None)
        task = Task(title=title, description=description, input_description=idescription,
                    output_description=odescription,
                    complexity=complexity, topics=topics, points=points)
        task.save()
        form = DocumentForm()
        # print(title, description, idescription, odescription, complexity, topics, points)
        return render(request, 'create_test_cases.html', {'task': task, 'form': form})

    else:
        # form = DocumentForm()
        return render(request, 'create_task.html')


def test_cases(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id', None)

        path = os.getcwd()
        print("The current working directory is %s" % path)
        path += "/media/tests/" + str(task_id)

        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        path += "/tests"
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        allTestCases = []

        for file_id in range(1, 100):
            myName = str(file_id) + "_field"
            testCase = request.POST.get(myName, None)
            if testCase is None:
                break
            file_name = "test-" + str(file_id) + ".in"
            with open(path + '/' + file_name, 'w+') as file:
                file.write(testCase)
            allTestCases.append(testCase)

        newdoc = Document(docfile=request.FILES['docfile'])
        path = path[:len(path)-5] # <- deleteing 'tests'

        with open(path + "authorSolution.py", 'wb') as file:
            file.write(newdoc.docfile.read())

        bash_files_path = os.getcwd() + "/media/bash_files/"
        shutil.copyfile(bash_files_path + "test.sh", path + "test.sh")
        shutil.copyfile(bash_files_path + "createCorrectOutputs.sh", path + "createCorrectOutputs.sh")

        st = os.stat(path + "test.sh")
        os.chmod(path + "test.sh", st.st_mode | stat.S_IEXEC)

        st = os.stat(path + "createCorrectOutputs.sh")
        os.chmod(path + "createCorrectOutputs.sh", st.st_mode | stat.S_IEXEC)

        subprocess.check_call([path + 'createCorrectOutputs.sh', 'python3 ' + path + 'authorSolution.py', path])

        task = Task.objects.get(id=task_id)

        return render(request, 'edit_task.html', {"task": task, "testCases": allTestCases})
    else:
        return render(request, '404_page.html')


def editTask(request, id):
    if request.method == 'POST':
        pass
    else:
        task = Task.objects.get(pk=id)
        testArray = ['a', 'b']
        return render(request, 'edit_task.html', {"task": task, "testArray": testArray})