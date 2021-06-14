import os
import pathlib
import shutil
import stat
import subprocess

from contester.models import *
from django.shortcuts import render

from contester.checker import checker
from contester.forms import *


def runscript(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = request.POST.get('task_id', None)
            newdoc = Document(docfile=request.FILES['docfile'], task_id=int(task_id), is_author_code=False)
            newdoc.save()

            print(newdoc.docfile)
            new_path = str(pathlib.Path(newdoc.docfile.path).parent) + '/' + str(newdoc.id) + str(
                pathlib.Path(newdoc.docfile.path).suffix)
            print(new_path)
            print(newdoc.docfile.name)

            os.rename(newdoc.docfile.path, new_path)
            newdoc.docfile.name = "codes/" + str(newdoc.id) + str(pathlib.Path(newdoc.docfile.path).suffix)
            newdoc.save()
            result, numberOfTestCases = checker(newdoc.docfile, task_id)
            res = 0
            for i in result:
                res += i

            task = Task.objects.get(pk=task_id)
            points = task.points * float(res / numberOfTestCases)
            is_accepted = False
            if res == numberOfTestCases:
                is_accepted = True
                countAccepted = Submit.objects.filter(user_id=request.user.id, task_id=task_id,
                                                      is_accepted=True).count()
                if countAccepted == 0:
                    task.user_counter += 1
                    task.save()

            all_submits = Submit.objects.filter(user_id=request.user.id, task_id=task_id)
            old_mx = 0
            for submit in all_submits:
                old_mx = max(old_mx, submit.points)

            new_mx = max(old_mx, points)
            curUser = Account.objects.get(pk=request.user.id)
            curUser.points -= old_mx
            curUser.points += new_mx
            curUser.save()

            new_submit = Submit(user_id=request.user.id, task_id=task_id, points=points, is_accepted=is_accepted,
                                document_id=newdoc.id)
            new_submit.save()

            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            taskLink = "http://127.0.0.1:8000/task/" + str(task_id)
            return render(request, 'task/results.html',
                          {'res': res, 'task_id': task_id, 'task': task, "taskLink": taskLink,
                           'totalNumOfTestCases': numberOfTestCases, "accepted": is_accepted})
    return render(request, 'task/results.html')


def suggest_task(request):
    return render(request, 'task/suggest_task.html')


def getTaskById(request, id):
    print(id)
    try:
        task = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        task = None

    if task is None:
        return render(request, '404_page.html')
    form = DocumentForm()
    my_submits_qs = Submit.objects.filter(user_id=request.user.id, task_id=id)
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
    author_code = None
    if has_accepted:
        author_code = Document.objects.all().filter(task_id=task.id, is_author_code=True).last()
        author_code = author_code.docfile.read().decode("utf-8")
    return render(request, 'task/task_page.html',
                  {'task': task, 'form': form, 'task_id': id, 'my_submits': my_submits,
                   'has_accepted': has_accepted, 'author_code': author_code})


def suggestingTask(request):
    form = SuggestingTaskForm()
    return render(request, "task/suggest_task.html", {"form": form})


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
        return render(request, 'task/create_test_cases.html', {'task': task, 'form': form})

    else:
        # form = DocumentForm()
        return render(request, 'task/create_task.html')


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

        newdoc = Document(docfile=request.FILES['docfile'], task_id=task_id, is_author_code=True)
        newdoc.save()
        path = path[:len(path) - 5]  # <- deleteing 'tests'

        with open(path + "authorSolution.py", 'wb') as file:
            file.write(newdoc.docfile.read())

        bash_files_path = os.getcwd() + "/media/bash_files/"
        shutil.copyfile(bash_files_path + "test.sh", path + "test.sh")
        shutil.copyfile(bash_files_path + "createCorrectOutputs.sh", path + "createCorrectOutputs.sh")

        st = os.stat(path + "test.sh")
        os.chmod(path + "test.sh", st.st_mode | stat.S_IEXEC)

        st = os.stat(path + "createCorrectOutputs.sh")
        os.chmod(path + "createCorrectOutputs.sh", st.st_mode | stat.S_IEXEC)

        try:
            subprocess.check_call([path + 'createCorrectOutputs.sh', 'python3 ' + path + 'authorSolution.py', path])
        except subprocess.CalledProcessError as e:
            print(e.output)
            print(e.cmd)
            print(e.returncode)
            print(e)
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

        example_number = int(request.POST.get("exampleNumber", None))
        example_number = min(example_number, len(allTestCases))
        task = Task.objects.get(id=task_id)
        task.sample_number = example_number

        if example_number >= 1:
            task.first_tc_input = allTestCases[0]
            with open(path + '/tests/test-1.out', 'r') as file:
                content = file.read()
            task.first_tc_output = content
        if example_number >= 2:
            task.second_tc_input = allTestCases[1]
            with open(path + '/tests/test-2.out', 'r') as file:
                content = file.read()
            task.second_tc_output = content
        if example_number >= 3:
            task.third_tc_input = allTestCases[2]
            with open(path + '/tests/test-3.out', 'r') as file:
                content = file.read()
            task.third_tc_output = content
        task.save()

        return render(request, 'task/task.html', {"task": task})
    else:
        return render(request, '404_page.html')


def editTask(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(pk=task_id)
        task.title = request.POST.get('title', None)
        task.description = request.POST.get('description', None)
        task.input_description = request.POST.get('idescription', None)
        task.output_description = request.POST.get('odescription', None)
        task.complexity = request.POST.get('complexity', None)
        task.topics = [request.POST.get('topics', None)]
        task.points = request.POST.get('points', None)
        task.save()
        contests = Contest.objects.all()
        tasks = Task.objects.all()
        return render(request, "index/HomePage.html", {'contests': contests, 'tasks': tasks})
    else:
        task = Task.objects.get(pk=task_id)
        complexityArray = ['Easy', 'Medium', 'Hard', 'Very Hard']
        topicsArray = ['Collections', 'String', 'Math', 'Data structure']

        for i in range(0, 4):
            if task.complexity == complexityArray[i]:
                tmp = complexityArray[i]
                complexityArray[i] = complexityArray[0]
                complexityArray[0] = tmp
                break

        for i in range(0, 4):
            if task.topics == topicsArray[i]:
                tmp = topicsArray[i]
                topicsArray[i] = topicsArray[0]
                topicsArray[0] = tmp
                break

        testCases = ['a', 'b']

        return render(request, 'task/edit_task.html',
                      {"task": task, "complexityArray": complexityArray, "topicsArray": topicsArray,
                       "testCases": testCases})
