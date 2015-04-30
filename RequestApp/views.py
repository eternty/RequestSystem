from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from RequestApp.models import User_type, Company, Request, Request_status, Specialization


@login_required(login_url='/signin')
def index(request):
    usertype = request.user.usertype.name
    if request.user.usertype.name == 'Engineer':

        requests = Request.objects.filter(group__in=request.user.get_specialization())
        myrequests = Request.objects.filter(engineer = request.user)

        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'engineer.html', context )

    elif request.user.usertype.name == 'Dispatcher':


        requests = Request.objects.filter(status__id = 2 )
        myrequests = Request.objects.filter(engineer = request.user)
        context = {
            'requests': requests,
            'myrequests': myrequests,
             'usertype': usertype
        }
        return render(request, 'disp.html', context)

    elif request.user.usertype.name == 'Client':

        requests = Request.objects.filter(company = request.user.company)
        myrequests = Request.objects.filter(creator = request.user)
        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'client.html', context)
    else:
        requests= Request.objects.exclude(status__id = 7 )
        newrequests = Request.objects.filter(status__id = 2)
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
        return render(request, 'SignIn.html' )

def hello(request):
	return HttpResponse("Hey You must be serious man, huh?")

def companypage(request):
    usertype = request.user.usertype.name
    clientcompany = Company.objects.get(name = request.user.company)
    manager = clientcompany.manager.get_full_name()
    focus = clientcompany.focus.get_full_name()
    context = {
            'clientcompany': clientcompany,
            'usertype': usertype,
            'manager': manager,
            'focus': focus
        }
    return render(request, 'companypage.html', context)
