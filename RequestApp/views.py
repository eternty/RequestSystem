from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from RequestApp.models import User_type, Company, Request,Request_status


@login_required(login_url='/signin')
def index(request):
    if request.user.usertype.name == 'Engineer':
        return render(request, 'Engineer.html', )
    elif request.user.usertype.name == 'Dispatcher':
        requests = Request.objects.filter(status__id = 2 )
        myrequests = Request.objects.filter(engineer = request.user)
        context = {
            'requests': requests,
            'myrequests': myrequests
        }
        return render(request, 'disp.html', context)
    else:
        return render(request, 'Client.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    else:
        return render(request, "SignIn.html" )

def hello(request):
	return HttpResponse("Hey You must be serious man, huh?")
def client(request):
    return render(request, "Client.html")
def dispatcher(request):
    return render(request, "Dispatcher.html")
def engineer(request):
    return render(request,"Engineer.html")
def new_req(request):
    return render(request,"New_request_client.html")
