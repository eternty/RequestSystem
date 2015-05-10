# coding=utf-8
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm, RequestForm, ClientRequestForm, ShowRequestForm, NewCommentForm


# Create your views here.
from RequestApp.models import User_type, Company, Request, Request_status, Specialization, System_User, Equipment, \
    Comment, Groups_engineer, Contract


@login_required(login_url='/signin')
def index(request):
    usertype = request.user.usertype.name
    if request.user.usertype.name == 'Engineer':

        requests = Request.objects.filter(group__in=request.user.get_specialization())
        myrequests = Request.objects.filter(engineer=request.user)

        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'engineer.html', context)

    elif request.user.usertype.name == 'Dispatcher':


        requests = Request.objects.filter(status__id=2)
        myrequests = Request.objects.filter(engineer=request.user)
        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'disp.html', context)

    elif request.user.usertype.name == 'Client':

        requests = Request.objects.filter(company=request.user.company)
        myrequests = Request.objects.filter(creator=request.user)
        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'client.html', context)
    else:
        requests = Request.objects.exclude(status__id=7)
        newrequests = Request.objects.filter(status__id=2)
        context = {
            'requests': requests,
            'newrequests': newrequests,
            'usertype': usertype
        }
        return render(request, 'manager.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    else:
        return render(request, 'signIn.html')


def hello(request):
    return HttpResponse("Hey You must be serious man, huh?")


def companiespage(request):
    usertype = request.user.usertype.name
    clientcompany = Company.objects.get(name=request.user.company)
    managername = clientcompany.manager.get_full_name()
    manager = System_User.objects.get(id=clientcompany.manager_id)
    focus = System_User.objects.get(id=clientcompany.focus_id)
    focusname = clientcompany.focus.get_full_name()
    companies = Company.objects.all()

    context = {
        'clientcompany': clientcompany,
        'usertype': usertype,
        'manager': manager,
        'focus': focus,
        'managername': managername,
        'focusname': focusname,
        'companies': companies
    }
    return render(request, 'companiespage.html', context)


def userspage(request):
    usertype = request.user.usertype.name
    clientusers = System_User.objects.filter(company=request.user.company)
    men = System_User.objects.exclude(usertype__name='Admin')

    context = {
        'clientusers': clientusers,
        'usertype': usertype,
        'men': men
    }
    return render(request, 'userspage.html', context)


def equipspage(request):
    usertype = request.user.usertype.name
    client_equips = Equipment.objects.filter(contract__company=request.user.company)
    equips = Equipment.objects.all()

    context = {
        'usertype': usertype,
        'client_equips': client_equips,
        'equips': equips
    }
    return render(request, 'equipspage.html', context)


def active_requests(request):
    act_requests = Request.objects.exclude(status__id=6)
    usertype = request.user.usertype.name
    context = {
        'act_requests': act_requests,
        'usertype': usertype
    }
    return render(request, 'active_requests.html', context)


def DetailCompany(request, pk):
    company = Company.objects.get(id=pk)
    usertype = request.user.usertype.name
    users = System_User.objects.filter(company=company)
    contracts = Contract.objects.filter(company = company)
    equips = Equipment.objects.filter(contract__company = company)
    managername = company.manager.get_full_name()
    manager = System_User.objects.get(id=company.manager_id)
    focus = System_User.objects.get(id=company.focus_id)
    focusname = company.focus.get_full_name()
    context = {
        'company': company,
        'usertype': usertype,
        'users':users,
        'contacts':contracts,
        'equips': equips,
        'managername':managername,
        'manager':manager,
        'focus':focus,
        'focusname':focusname

    }
    return render(request, 'сompany.html', context)


def test(request):
    usertype = request.user.usertype.name
    context = {
        'usertype': usertype
    }
    return render(request, 'your-name.html', context)


def get_name(request):
    usertype = request.user.usertype.name

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['your_name']
            context = {
                'name': name,
                'usertype': usertype,

            }
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'results.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'your-name.html', {'form': form, 'usertype': usertype})


def results(request):
    usertype = request.user.usertype.name

    context = {

        'usertype': usertype
    }
    return render(request, 'results.html', context)


def new_request(request):
    usertype = request.user.usertype.name
    if usertype !='Client':
        if request.method == 'POST':
            form = RequestForm(request.POST)
            if form.is_valid():
                new_request = form.save(commit=False)
                new_request.status = Request_status.objects.get(id= 1)
                new_request.save()

                context = {
                    'created_request': new_request,
                    'form': form,
                    'usertype': usertype,
                    'username': request.user.get_full_name(),
                }
                return render(request, 'created_request.html', context)
        else:
            form = RequestForm()
            context = {

                'form': form,
                'usertype': request.user.usertype.name
            }
            return render(request, 'my_request.html', context)

    else:
        if request.method == 'POST':
            form = ClientRequestForm(request.POST)
            if form.is_valid():
                new_request = form.save(commit=False)
                new_request.company = request.user.company
                new_request.creator = request.user
                new_request.status = Request_status.objects.get(id= 1)
                new_request.save()
                context = {
                    'created_request': new_request,
                    'form': form,
                    'usertype': usertype,
                    'username': request.user.get_full_name(),
                }
                return render(request, 'created_request.html', context)
        else:
            form = ClientRequestForm()
            context = {
                'form': form,
                'usertype': request.user.usertype.name
            }
            return render(request, 'my_request.html', context)

def created_request(request):
    return render(request, 'created_request.html', )

def request_journal(request, pk):
#to be ended

    usertype = request.user.usertype.name
    commentform = NewCommentForm()
    comments = Comment.objects.filter(request__id = pk)
    equips = Equipment.objects.filter()

    if request.method == 'POST':
        our_request = Request.objects.get(id = pk)
        changed_form = ShowRequestForm(request.POST)
        changed_form.save(commit=False)
        if changed_form.is_valid():
            our_request.engineer = changed_form.cleaned_data['engineer']
            our_request.group = changed_form.cleaned_data['group']
            our_request.dispatcher = changed_form.cleaned_data['dispatcher']
            our_request.creator = changed_form.cleaned_data['creator']
            our_request.equipment = changed_form.cleaned_data['equipment']
            our_request.priority = changed_form.cleaned_data['priority']
            our_request.reqtype = changed_form.cleaned_data['reqtype']
            our_request.status = changed_form.cleaned_data['status']
            our_request.save()
            reqform = ShowRequestForm(instance=our_request)
            context = {
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request
            }

        else:
            return HttpResponse("Error!")

    else:
        our_request = Request.objects.get(id = pk)
        reqform= ShowRequestForm(instance = our_request)
        context = {
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request,
                'equips':equips
        }

    return render(request, 'request_journal.html', context)

def add_comment(request, pk):
    usertype = request.user.usertype.name
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        commentform = NewCommentForm(request.POST)
        # check whether it's valid:
        if commentform.is_valid():
            creating_comment = commentform.save(commit=False)
            creating_comment.author = request.user
            creating_comment.request = Request.objects.get(id = pk)
            creating_comment.save()
            needed_request = Request.objects.get(id = pk)
            reqform= ShowRequestForm(instance = needed_request)
            comments = Comment.objects.filter(request__id = pk)
            commentform2= NewCommentForm()
            context = {

                'usertype': usertype,
                'reqform': reqform,
                'comments': comments,
                'commentform': commentform2,
                'reqobject': needed_request

            }
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'request_journal.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        usertype = request.user.usertype.name
        commentform = NewCommentForm()
        context = {
                'pk': pk,
                'usertype': usertype,
                'commentform': commentform
            }


    return render(request, 'request_journal.html', context)


def get_engineers_by_group(request):
    group_id = request.GET.get('group_id')

    if group_id:
        ids = Specialization.objects.values_list('engineer_id', flat=True).filter(group__id=int(group_id))
    else:
        ids = []

    return HttpResponse(json.dumps({'ids': list(ids)}), content_type='application/json')


def user(request, pk):
    usertype = request.user.usertype.name
    user = System_User.objects.get(id = pk)
    active_requests = Request.objects.exclude(status__id = 6)
    open_requests = active_requests.filter(creator = user)
    work_on_request = active_requests.filter(engineer = user)
    open_dispatched_req = active_requests.filter(dispatcher = user)
    context = {
        'usertype': usertype,
        'user': user,
        'open_requests':open_requests,
        'work_on_request':work_on_request,
        'open_dispatched_req':open_dispatched_req
    }
    return render(request,'User.html', context)