# coding=utf-8
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import  RequestForm, ClientRequestForm, ShowRequestForm, NewCommentForm, ShowClientRequestForm, ShowEngRequestForm, \
    ShowEngSolRequestForm, ShowSolRequestForm


# Create your views here.
from RequestApp.models import User_type, Company, Request, Request_status, Specialization, System_User, Equipment, \
    Comment, Groups_engineer, Contract, Replacement, Request_priority, Normative_time, Execution_time


@login_required(login_url='/signin')
def index(request):
    usertype = request.user.usertype.name
    if request.user.usertype.name == u'Инженер':
        active_requests = Request.objects.exclude(status__name = u'Завершена')
        requests = active_requests.filter(group__in=request.user.get_specialization())
        myrequests = Request.objects.filter(engineer=request.user)
        requests.order_by('-createtime','reqtype')
        myrequests.order_by('-createtime','reqtype')
        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'engineer.html', context)

    elif request.user.usertype.name == u'Диспетчер':

        active_requestss = Request.objects.exclude(status__name = u'Завершена')
        requests = Request.objects.filter(status__name = u'Зарегистрирована')
        requests.order_by('-createtime','reqtype')
        myrequests = active_requestss.filter(engineer = request.user)
        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'disp.html', context)

    elif request.user.usertype.name == u'Клиент':

        requests = Request.objects.filter(company=request.user.company)
        myrequests = Request.objects.filter(creator=request.user)
        context = {
            'requests': requests,
            'myrequests': myrequests,
            'usertype': usertype
        }
        return render(request, 'client.html', context)
    else:
        requests = Request.objects.exclude(status__name = u'Завершена')
        newrequests = Request.objects.filter(status__name = u'Зарегистрирована')
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

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("/")
            else:
                return HttpResponse("Disabled account!")
        else:
            return render(request, 'signin_page.html')

    else:
        return render(request, 'signin_page.html')


def logout_view(request):
    logout(request)
    return render(request,'logout.html')


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
    act_requests = Request.objects.exclude(status__name=u'Завершена')
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


def new_request(request):
    usertype = request.user.usertype.name
    if usertype != u'Клиент':
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
            form.fields["equipment"].queryset = Equipment.objects.filter(company__id=request.user.company.id)
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
            form.fields["equipment"].queryset = Equipment.objects.filter(company__id=request.user.company.id)
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
    comments = Comment.objects.filter(request__id=pk)

    if request.method == 'POST':

        our_request = Request.objects.get(id=pk)
        if our_request.status.id >6:
            sol = True
            changed_form = ShowSolRequestForm(request.POST)
        else:
            sol = False
            changed_form = ShowRequestForm(request.POST)
        #changed_form.save(commit=False)
        company = our_request.company
        equips = Equipment.objects.filter(contract__company=company )

        if changed_form.is_valid():
            our_request.engineer = changed_form.cleaned_data['engineer']
            our_request.group = changed_form.cleaned_data['group']
            our_request.dispatcher = changed_form.cleaned_data['dispatcher']
            our_request.creator = changed_form.cleaned_data['creator']
            our_request.equipment = changed_form.cleaned_data['equipment']
            our_request.priority = changed_form.cleaned_data['priority']
            our_request.reqtype = changed_form.cleaned_data['reqtype']
            if sol:
                our_request.solution = changed_form.cleaned_data['solution']
            new_stat = Request_status.objects.get(name=changed_form.cleaned_data['status'])
            if our_request.status.id != new_stat.id:
                exec_time = Execution_time.objects.create(request=our_request, rstatus=changed_form.cleaned_data['status'] )
                exec_time.save()
                our_request.status = changed_form.cleaned_data['status']
            our_request.save()
            if our_request.status.id >6:
                reqform = ShowSolRequestForm (instance=our_request)
            else:
                reqform = ShowRequestForm(instance=our_request)

            context = {
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request,
                'equips': equips
            }

        else:
            return HttpResponse("Error!")

    else:
        our_request = Request.objects.get(id=pk)
        if our_request.status.id >6:
            reqform = ShowSolRequestForm (instance=our_request)
        else:
            reqform = ShowRequestForm(instance=our_request)
        company = our_request.company
        equips = Equipment.objects.filter(contract__company=company )
        context = {
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request,
                'equips':equips
        }

    return render(request, 'request_journal.html', context)

def engineer_request_journal(request, pk):
#to be ended

    usertype = request.user.usertype.name
    commentform = NewCommentForm()
    comments = Comment.objects.filter(request__id=pk)

    if request.method == 'POST':

        our_request = Request.objects.get(id=pk)
        if our_request.status.id >6:
            sol = True
            changed_form = ShowEngSolRequestForm(request.POST)
        else:
            sol = False
            changed_form = ShowEngRequestForm(request.POST)
        changed_form.save(commit=False)
        company = our_request.company
        equips = Equipment.objects.filter(contract__company=company )

        if changed_form.is_valid():

            our_request.engineer = changed_form.cleaned_data['engineer']
            our_request.group = changed_form.cleaned_data['group']
            if sol:
                our_request.solution = changed_form.cleaned_data['solution']
            our_request.equipment = changed_form.cleaned_data['equipment']
            new_stat = Request_status.objects.get(name=changed_form.cleaned_data['status'])
            if our_request.status.id != new_stat.id:
                exec_time = Execution_time.objects.create(request=our_request, rstatus=changed_form.cleaned_data['status'] )
                exec_time.save()
                our_request.status = changed_form.cleaned_data['status']
            #our_request.equipment = changed_form.cleaned_data['equipment1']
            our_request.save()
            if our_request.status.id >6:
                reqform = ShowEngSolRequestForm (instance=our_request)
            else:
                reqform = ShowEngRequestForm(instance=our_request)
            context = {
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request,
                'equips': equips
            }

        else:
            return HttpResponse("Error!")

    else:

        our_request = Request.objects.get(id=pk)
        if our_request.status.id >6:
            reqform = ShowEngSolRequestForm (instance=our_request)
        else:
            reqform = ShowEngRequestForm(instance=our_request)
        company = our_request.company
        equips = Equipment.objects.filter(contract__company=company )
        context = {
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request,
                'equips':equips
        }

    return render(request, 'engineer_request_journal.html', context)


def client_request_journal(request, pk):
    usertype = request.user.usertype.name
    commentform = NewCommentForm()
    comments = Comment.objects.filter(request__id=pk)

    if request.method == 'POST':
        our_request = Request.objects.get(id = pk)
        changed_form = ShowClientRequestForm(request.POST)

        changed_form.save(commit=False)
        company = our_request.company
        equips = Equipment.objects.filter(contract__company=company)

        if changed_form.is_valid():

            our_request.approvement = changed_form.cleaned_data['approvement']
            our_request.save()
            reqform = ShowClientRequestForm(instance=our_request)
            if our_request.status >6:
                if our_request.solution != None:
                    need_approve = True
            else:
                need_approve = False
            context = {
                #'need_approve': need_approve,
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request,
                'equips': equips,
                'need_approve': need_approve
            }

        else:
            return HttpResponse("Error!")

    else:
        our_request = Request.objects.get(id = pk)
        reqform= ShowClientRequestForm(instance = our_request)

        company = our_request.company
        equips = Equipment.objects.filter(contract__company = company )
        if our_request.status >6:
            if our_request.solution != None:
                need_approve = True
            else:
                need_approve = False
        context = {
                'need_approve': need_approve,
                'reqform': reqform,
                'usertype': usertype,
                'comments': comments,
                'commentform': commentform,
                'reqobject': our_request,
                'equips':equips
        }

    return render(request, 'client_request_journal.html', context)


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


def client_add_comment(request, pk):
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

            return render(request, 'client_request_journal.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        usertype = request.user.usertype.name
        commentform = NewCommentForm()
        context = {
                'pk': pk,
                'usertype': usertype,
                'commentform': commentform
            }


    return render(request, 'client_request_journal.html', context)


def engineer_add_comment(request, pk):
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
            reqform= ShowEngRequestForm(instance = needed_request)
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

            return render(request, 'engineer_request_journal.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        usertype = request.user.usertype.name
        commentform = NewCommentForm()
        context = {
                'pk': pk,
                'usertype': usertype,
                'commentform': commentform
            }


    return render(request, 'engineer_request_journal.html', context)


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
    opened_requests = active_requests.filter(creator = user)
    work_on_request = active_requests.filter(engineer = user)
    open_dispatched_req = active_requests.filter(dispatcher = user)
    context = {
        'role': user.usertype,
        'usertype': usertype,
        'user': user,
        'open_requests':opened_requests,
        'work_on_request':work_on_request,
        'open_dispatched_req':open_dispatched_req
    }
    return render(request,'User.html', context)

def equipment(request, pk):
    usertype = request.user.usertype.name
    equip = Equipment.objects.get(id = pk)
    company = equip.contract.get_company()
    exreplaces = Equipment.objects.filter(replace__in= equip.get_replacement())
    replaces = Replacement.objects.filter(crashed = equip)
    requests = Request.objects.filter(equipment = equip)
    context = {
        'equip':equip,
        'usertype': usertype,
        'company': company,
        'replaces': replaces,
        'requests': requests
    }
    return render(request,'equipment.html', context)


def normative_time(request):
    accidents = Normative_time.objects.filter(reqtype = u'Аварийная ситуация')
    services = Normative_time.objects.filter(reqtype = u'Запрос на обслуживание')
    changes = Normative_time.objects.filter(reqtype = u'Запрос на изменение')

    critical_accidents = accidents.filter(priority = u'Критический')
    high_accidents = accidents.filter(priotiry = u'Высокий')
    middle_accidents = accidents.filter(priority = u'Средний')
    low_accidents = accidents.filter(priority = u'Низкий')

    critical_services = services.filter(priority = u'Критический')
    high_services  = services.filter(priotiry = u'Высокий')
    middle_services  = services.filter(priority = u'Средний')
    low_services  = services.filter(priority = u'Низкий')

    critical_changes = changes.filter(priority = u'Критический')
    high_changes  = changes.filter(priotiry = u'Высокий')
    middle_changes  = changes.filter(priority = u'Средний')
    low_changes  = changes.filter(priority = u'Низкий')


    context = {
        'critical_accidents': critical_accidents,
        'high_accidents': high_accidents,
        'middle_accidents': middle_accidents,
        'low_accidents': low_accidents,

        'critical_services': critical_services,
        'high_services': high_services,
        'middle_services': middle_services,
        'low_services': low_services,

        'critical_changes': critical_changes,
        'high_changes': high_changes,
        'middle_changes': middle_changes,
        'low_changes': low_changes
    }
    return render(request,'normative_time.html', context)


def get_equipment(request, pk):
    usertype = request.user.usertype.name
    replacement = Replacement.objects.get(id = pk)
    equip = Equipment.objects.get(id = replacement.replace.id)
    company = equip.contract.get_company()
    replaces = Replacement.objects.filter(crashed = equip)
    requests = Request.objects.filter(equipment = equip)
    context = {
        'equip':equip,
        'usertype': usertype,
        'company': company,
        'replaces': replaces,
        'requests': requests
    }
    return render(request,'equipment.html', context)


def req_archive(request):
    usertype = request.user.usertype.name
    done_requests = Request.objects.filter(status__name=u'Завершена')
    company = request.user.company
    name_company = company.name
    comp_requests = done_requests.filter(company=company)
    context = {
        'name_company': name_company,
        'usertype': usertype,
        'company': company,
        'comp_requests': comp_requests,
        'requests': done_requests
    }
    return render(request,'req_archive.html', context)